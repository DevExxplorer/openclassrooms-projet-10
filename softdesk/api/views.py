from django.db import IntegrityError
from django.http import Http404
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied
from rest_framework.viewsets import ModelViewSet

from api.models import CustomUser, Project, Issue, Contributor, Comment
from api.permissions import IsAuthor, IsProjectContributor, IsSelf
from api.serializers.user import UserSerializer
from api.serializers.project import ProjectSerializer
from api.serializers.issue import IssueSerializer
from api.serializers.contributor import ContributorSerializer
from api.serializers.comment import CommentSerializer


class UserViewSet(ModelViewSet):
    """
       ViewSet pour gérer les utilisateurs (CustomUser).
       Permet d'obtenir la liste des utilisateurs et de les afficher, de manière authentifiée.
   """
    serializer_class = UserSerializer
    permission_classes = [IsSelf]

    def get_queryset(self):
        """
           Retourne la liste des utilisateurs, triée par date d'inscription (du plus récent au plus ancien).
       """
        return CustomUser.objects.all().order_by('-date_joined')


class CommentViewSet(ModelViewSet):
    """
    ViewSet pour gérer les commentaires sur les issues.
    Les utilisateurs doivent être contributeurs du projet pour pouvoir commenter.
    """
    serializer_class = CommentSerializer

    def get_queryset(self):
        """
        Retourne la liste des commentaires associés à une issue spécifique.
        """
        issue_id = self.kwargs["issue_pk"]
        return Comment.objects.filter(issue_id=issue_id)

    def perform_create(self, serializer):
        """
        Crée un nouveau commentaire pour une issue et l'associe à l'utilisateur et au projet.
        Vérifie que l'utilisateur est un contributeur du projet avant de permettre la création.
        """
        user = self.request.user

        project_id = self.kwargs.get('project_pk')
        project = Project.objects.get(id=project_id)

        issue_id = self.kwargs.get('issue_pk')
        issue = Issue.objects.get(id=issue_id)

        contributor = Contributor.objects.filter(project=project, user=user).first()

        if not contributor:
            raise ValidationError("You are not a contributor to this project.")

        issue = serializer.save(issue=issue, author=contributor)

    def get_permissions(self):
        """
       Définit les permissions pour cette vue. Seuls les contributeurs authentifiés peuvent commenter.
       """
        return [IsAuthenticated(), IsProjectContributor()]


####################

class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer

    def get_permissions(self):
        """
        Gestion des permissions
        """
        print('SELF', self.action)
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthor()]
        elif self.action in ['create']:
            return [IsAuthenticated()]

        return [IsProjectContributor()]


    def get_queryset(self):
        """
        Récupére la liste des projets ou est present le contributeur
        """
        user = self.request.user
        return Project.objects.filter(contributors_project__user=user)


    def get_object(self):
        """
        Surcharge la methode get_objecct() pour pouvoir personnaliser le message d'erreur
        """
        try:
            return super().get_object()
        except Http404:
            raise NotFound("Ce projet n'existe pas ou vous n'êtes pas contributeur de ce projet")


    def perform_create(self, serializer):
        """
        Lors de la création d'un projet
        La function rajoute les informations de l'auteur et du contributeur
        """
        user = self.request.user

        project = serializer.save()
        contributor = Contributor.objects.create(user=user, project=project)
        project.author = contributor
        project.save()


class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorSerializer

    def get_permissions(self):
        """
        Gestion des permissions
        """
        if self.action in ['list', 'retrieve']:
            return  [IsProjectContributor()]
        elif self.action in ['create', 'destroy']:
            return  [IsAuthor()]

        raise PermissionDenied("Action non autorisée.")

    def get_project_id(self):
        """
        Retourne le projet id
        """
        return self.kwargs.get('project_pk')

    def get_queryset(self):
        """
          Retourne les contributeurs du projet si l'utilisateur en fait partie.
        """
        is_contributor = Contributor.objects.filter(project_id=self.get_project_id(), user=self.request.user).exists()

        if not is_contributor:
            raise PermissionDenied("Vous n'êtes pas contributeur de ce projet.")

        return Contributor.objects.filter(project_id=self.get_project_id())

    def perform_create(self, serializer):
        """
        Crée un contributeur lié au projet courant.
        """
        try:
            serializer.save(project_id=self.get_project_id())
        except IntegrityError:
            raise ValidationError({"detail": "Ce contributeur est déjà ajouté à ce projet."})

    def perform_destroy(self, instance):
        """
        Supprime le contributeur spécifié du projet.
        """
        instance.delete()


class IssueViewSet(ModelViewSet):
    serializer_class = IssueSerializer

    def get_permissions(self):
        """
        Gestion des permissions
        """
        if self.action in ['list', 'retrieve']:
            return  [IsProjectContributor()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthor()]

        raise PermissionDenied("Action non autorisée.")

    def get_queryset(self):
        project_id = self.kwargs.get('project_pk')
        return Issue.objects.filter(project_id=project_id)

    def perform_create(self, serializer):
        user = self.request.user

        project_id = self.kwargs.get('project_pk')
        project = Project.objects.get(id=project_id)

        contributor = Contributor.objects.filter(project=project, user=user).first()

        if not contributor:
            raise ValidationError("You are not a contributor to this project.")

        serializer.save(project=project, author=contributor)
