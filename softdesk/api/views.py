from django.db import IntegrityError
from django.db.models import Q

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
    permission_classes = [IsAuthenticated, IsAuthor]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(
            Q(contributors_project__user=user) | Q(author=user)
        ).distinct()

    def perform_create(self, serializer):
        user = self.request.user
        project = serializer.save(author=user)


###
class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorSerializer

    def get_project_id(self):
        return self.kwargs.get('project_pk')

    def get_queryset(self):
        is_contributor = Contributor.objects.filter(project_id=self.get_project_id(), user=self.request.user).exists()

        if not is_contributor:
            raise PermissionDenied("Vous n'êtes pas contributeur de ce projet.")

        return Contributor.objects.filter(project_id=self.get_project_id())

    def perform_create(self, serializer):
        try:
            serializer.save(project_id=self.get_project_id())
        except IntegrityError:
            raise ValidationError({"detail": "Ce contributeur est déjà ajouté à ce projet."})

    def perform_destroy(self, instance):
        instance.delete()

##
class IssueViewSet(ModelViewSet):
    serializer_class = IssueSerializer

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

##@
class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        issue_id = self.kwargs["issue_pk"]
        return Comment.objects.filter(issue_id=issue_id)

    def perform_create(self, serializer):
        user = self.request.user

        project_id = self.kwargs.get('project_pk')
        project = Project.objects.get(id=project_id)

        issue_id = self.kwargs.get('issue_pk')
        issue = Issue.objects.get(id=issue_id)

        contributor = Contributor.objects.filter(project=project, user=user).first()

        if not contributor:
            raise ValidationError("You are not a contributor to this project.")

        issue = serializer.save(issue=issue, author=contributor)