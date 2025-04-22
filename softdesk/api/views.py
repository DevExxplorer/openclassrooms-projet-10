from django.db import IntegrityError
from django.db.models import Q
from rest_framework.generics import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.viewsets import ModelViewSet

from api.models import CustomUser, Project, Issue, Contributor, Comment
from api.permissions import IsAuthor
from api.serializers import UserSerializer, ProjectSerializer, IssueSerializer, ContributorSerializer, CommentSerializer


class UserViewSet(ModelViewSet):
    """
       API endpoint permettant de gérer les utilisateurs.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retourne l'ensemble des utilisateurs si l'utilisateur connecté est admin,
        sinon retourne uniquement ses propres informations.
        """
        user = self.request.user

        if self.action != 'retrieve' and user.is_superuser:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=user.id)

    def perform_create(self, serializer):
        """
             Crée un nouvel utilisateur uniquement si l'utilisateur connecté est un admin.
         """
        user = self.request.user

        if not user.is_superuser:
            raise PermissionDenied("Only admins can create users.")

        serializer.save()


class ProjectViewSet(ModelViewSet):
    """
    API endpoint permettant de gérer les projets.
    """

    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
          Retourne la liste des projets pour lesquels l'utilisateur connecté est
          soit auteur, soit contributeur.
       """
        user = self.request.user
        return Project.objects.filter(
            Q(contributors_project__user=user) | Q(author=user)
        ).distinct()

    def perform_create(self, serializer):
        """
           Crée un nouveau projet avec l'utilisateur connecté comme auteur,
           et l'ajoute automatiquement comme contributeur au projet.
       """
        user = self.request.user
        project = serializer.save(author=user)

        project.contributors_project.create(
            user=user,
            project=project,
        )

    def get_permissions(self):
        """
        Détermine dynamiquement les permissions :
        IsAuthenticated pour toutes les actions
        IsAuthor ajouté pour les actions de modification et suppression
        """
        permissions = [IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions.append(IsAuthor())
        return permissions


class ContributorViewSet(ModelViewSet):
    """
    API endpoint pour gérer les contributeurs d'un projet.
    """
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']

    def get_project_id(self):
        """
        Récupère l'identifiant du projet depuis l'URL.
        """
        return self.kwargs.get('project_pk')

    def get_queryset(self):
        """
        Liste les contributeurs associés au projet spécifié.
        """
        return Contributor.objects.filter(
            project_id=self.get_project_id(),
        )

    def perform_create(self, serializer):
        """
        Ajoute un contributeur à un projet.
        Lève une erreur si le contributeur est déjà ajouté.
        """
        try:
            project = get_object_or_404(Project, pk=self.get_project_id())
            serializer.save(project=project)
        except IntegrityError:
            raise ValidationError({"detail": "Ce contributeur est déjà ajouté à ce projet."})

    def perform_destroy(self, instance):
        """
        Supprime un contributeur, sauf s’il est l’auteur du projet.
        """
        project = instance.project
        if instance.user == project.author:
            raise ValidationError({"detail": "Impossible de supprimer l'auteur du projet."})

        instance.delete()


class IssueViewSet(ModelViewSet):
    """
    API endpoint pour gérer les issues d’un projet.
    """
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Liste les issues associées à un projet spécifique.
        """
        user = self.request.user
        project_pk = self.kwargs.get('project_pk')

        is_contributor = Contributor.objects.filter(
            project_id=project_pk,
            user=user
        ).exists()

        if not is_contributor:
            return Issue.objects.none()

        return Issue.objects.filter(project_id=project_pk)

    def perform_create(self, serializer):
        """
        Crée une nouvelle issue pour le projet spécifié,
        avec l’utilisateur connecté comme auteur.
        """
        user = self.request.user
        project_pk = self.kwargs.get('project_pk')
        project = Project.objects.get(id=project_pk)
        serializer.save(project=project, author=user)

    def get_permissions(self):
        """
        Applique IsAuthenticated à toutes les actions,
        et ajoute IsAuthor uniquement à la suppression.
        """
        permissions = [IsAuthenticated()]
        if self.action in ['destroy']:
            permissions.append(IsAuthor())
        return permissions


class CommentViewSet(ModelViewSet):
    """
        API endpoint pour gérer les commentaires liés à une issue.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Liste les commentaires associés à une issue spécifique.
        """
        user = self.request.user
        issue_id = self.kwargs["issue_pk"]
        issue = Issue.objects.get(id=issue_id)

        is_contributor = Contributor.objects.filter(
            project_id=issue.project.id,
            user=user
        ).exists()

        if not is_contributor:
            return Comment.objects.none()

        return Comment.objects.filter(issue_id=issue_id)

    def perform_create(self, serializer):
        """
       Crée un commentaire lié à une issue,
       avec l’utilisateur connecté comme auteur.
       """
        user = self.request.user

        issue_id = self.kwargs.get('issue_pk')
        issue = Issue.objects.get(id=issue_id)

        issue = serializer.save(issue=issue, author=user)

    def get_permissions(self):
        """
        Applique IsAuthenticated à toutes les actions,
        et ajoute IsAuthor pour les actions de modification et suppression.
        """
        permissions = [IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions.append(IsAuthor())
        return permissions
