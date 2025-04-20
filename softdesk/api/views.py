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
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if self.action != 'retrieve' and user.is_superuser:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=user.id)

    def perform_create(self, serializer):
        user = self.request.user

        if not user.is_superuser:
            raise PermissionDenied("Only admins can create users.")

        serializer.save()


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(
            Q(contributors_project__user=user) | Q(author=user)
        ).distinct()

    def perform_create(self, serializer):
        """
        Creation d'un nouveau projet
        """
        user = self.request.user
        project = serializer.save(author=user)

        project.contributors_project.create(
            user = user,
            project=project,
        )

    def get_permissions(self):
        """
        Applique IsAuthenticated à toutes les actions,
        et ajoute IsAuthor uniquement au méthode update et delete
        """
        permissions = [IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions.append(IsAuthor())
        return permissions


class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']

    def get_project_id(self):
        return self.kwargs.get('project_pk')

    def get_queryset(self):
        return Contributor.objects.filter(
            project_id=self.get_project_id(),
        )

    def perform_create(self, serializer):
        try:
            project = get_object_or_404(Project, pk=self.get_project_id())
            serializer.save(project=project)
        except IntegrityError:
            raise ValidationError({"detail": "Ce contributeur est déjà ajouté à ce projet."})

    def perform_destroy(self, instance):
        project = instance.project
        if instance.user == project.author:
            raise ValidationError({"detail": "Impossible de supprimer l'auteur du projet."})

        instance.delete()


class IssueViewSet(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_pk = self.kwargs.get('project_pk')
        return Issue.objects.filter(project_id=project_pk)

    def perform_create(self, serializer):
        user = self.request.user
        project_pk = self.kwargs.get('project_pk')
        project = Project.objects.get(id=project_pk)
        serializer.save(project=project, author=user)

    def get_permissions(self):
        """
        Applique IsAuthenticated à toutes les actions,
        et ajoute IsAuthor uniquement au méthode update et delete
        """
        permissions = [IsAuthenticated()]
        if self.action in ['destroy']:
            permissions.append(IsAuthor())
        return permissions


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        issue_id = self.kwargs["issue_pk"]
        return Comment.objects.filter(issue_id=issue_id)

    def perform_create(self, serializer):
        user = self.request.user

        project_id = self.kwargs.get('project_pk')
        project = Project.objects.get(id=project_id)

        issue_id = self.kwargs.get('issue_pk')
        issue = Issue.objects.get(id=issue_id)

        issue = serializer.save(issue=issue, author=user)

    def get_permissions(self):
        """
        Applique IsAuthenticated à toutes les actions,
        et ajoute IsAuthor uniquement au méthode update et delete
        """
        permissions = [IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions.append(IsAuthor())
        return permissions