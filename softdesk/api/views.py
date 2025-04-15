from django.db import IntegrityError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet

from api.models import CustomUser, Project, Issue, Contributor, Comment
from api.permissions import IsAuthor, IsContributorAuthenticated
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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
           Retourne la liste des utilisateurs, triée par date d'inscription (du plus récent au plus ancien).
       """
        return CustomUser.objects.all().order_by('-date_joined')


class ProjectViewSet(ModelViewSet):
    """
       ViewSet pour gérer les projets.
       Permet de lister, créer, récupérer, mettre à jour et supprimer des projets.
       L'utilisateur doit être authentifié et, dans certains cas, être contributeur du projet.
   """
    serializer_class = ProjectSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthor()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """
           Retourne la liste de tous les projets.
        """
        user = self.request.user
        return Project.objects.filter(contributors_project__user=user)

    def get_object(self):
        """
        Récupère un projet spécifique et vérifie que l'utilisateur est contributeur.
        """
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializer):
        """
            Crée un nouveau projet et assigne l'utilisateur connecté comme contributeur et auteur du projet.
        """
        user = self.request.user

        project = serializer.save()
        contributor = Contributor.objects.create(user=user, project=project)
        project.author = contributor
        project.save()


class IssueViewSet(ModelViewSet):
    """
    ViewSet pour gérer les issues d'un projet.
    Les utilisateurs doivent être des contributeurs pour pouvoir interagir avec les issues.
    """
    serializer_class = IssueSerializer
    permission_classes = [IsContributorAuthenticated]

    def get_queryset(self):
        """
       Retourne la liste des issues associées à un projet spécifique.
       """
        project_id = self.kwargs.get('project_pk')
        return Issue.objects.filter(project_id=project_id)

    def perform_create(self, serializer):
        """
        Crée une nouvelle issue et l'associe à un projet.
        Vérifie que l'utilisateur est un contributeur du projet avant de permettre la création.
        """
        user = self.request.user

        project_id = self.kwargs.get('project_pk')
        project = Project.objects.get(id=project_id)

        contributor = Contributor.objects.filter(project=project, user=user).first()

        if not contributor:
            raise ValidationError("You are not a contributor to this project.")

        serializer.save(project=project, author=contributor)

    def get_permissions(self):
        """
        Définit les permissions pour cette vue. Seuls les contributeurs authentifiés peuvent créer ou interagir avec des issues.
        """
        return [IsAuthenticated(), IsContributorAuthenticated()]


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
        return [IsAuthenticated(), IsContributorAuthenticated()]


class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthor]

    def get_permissions(self):
        if self.request.method in ['GET', 'POST', 'DELETE']:
            return [IsAuthor()]
        return [IsContributorAuthenticated()]

    def get_project_id(self):
        """
        Retourne l'id du projet
        """
        return self.kwargs.get('project_pk')

    def get_queryset(self):
        """
        Retourne les contributeurs associés au projet.
        """
        return Contributor.objects.filter(project_id=self.get_project_id())

    def perform_create(self, serializer):
        """
        Crée un nouveau contributeur pour le projet.
        """
        try:
            serializer.save(project_id=self.get_project_id())
        except IntegrityError:
            raise ValidationError({"detail": "Ce contributeur est déjà ajouté à ce projet."})


    def perform_destroy(self, instance):
        """
        Supprime un contributeur
        """
        print(f"Suppression de : {instance}")
        instance.delete()
