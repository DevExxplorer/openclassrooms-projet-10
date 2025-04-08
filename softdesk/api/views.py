from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet

from api.models import CustomUser, Project, Issue, Contributor, Comment
from api.permissions import IsContributorAuthenticated
from api.serializers.user import UserSerializer
from api.serializers.project import ProjectSerializer
from api.serializers.issue import IssueSerializer
from api.serializers.contributor import ContributorSerializer
from api.serializers.comment import CommentSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.all().order_by('-date_joined')


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.all()

    def perform_create(self, serializer):
        user = self.request.user

        project = serializer.save()
        contributor = Contributor.objects.create(user=user, project=project)
        project.author = contributor
        project.save()

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsContributorAuthenticated()]
        return [IsAuthenticated()]


class IssueViewSet(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsContributorAuthenticated]
    
    def get_queryset(self):
        project_id = self.kwargs.get('project_pk')
        return Issue.objects.filter(project_id=project_id)

    def perform_create(self, serializer):
        # On récupere l'utilisateur connecté et on verifie que celui ci fait partie des contributeurs du projet
        user = self.request.user

        project_id = self.kwargs.get('project_pk')
        project = Project.objects.get(id=project_id)

        # On récupère les contributeurs du projet
        contributor = Contributor.objects.filter(project=project, user=user).first()

        # Vérifier si l'utilisateur est un contributeur du projet
        if not contributor:
            raise ValidationError("You are not a contributor to this project.")

        # On sauvegarde l'issue en associant le projet
        issue = serializer.save(project=project, author=contributor)

    def get_permissions(self):
        return [IsAuthenticated(), IsContributorAuthenticated()]


class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorSerializer

    def get_queryset(self):
        project_id = self.kwargs.get('project_pk')
        return Contributor.objects.filter(project_id=project_id)

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_pk')
        project = Project.objects.get(id=project_id)
        serializer.save(project=project)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        issue_id = self.kwargs["issue_pk"]
        return Comment.objects.filter(issue_id=issue_id)

    def perform_create(self, serializer):
        # On récupere l'utilisateur connecté et on verifie que celui ci fait partie des contributeurs du projet
        user = self.request.user

        project_id = self.kwargs.get('project_pk')
        project = Project.objects.get(id=project_id)

        issue_id = self.kwargs.get('issue_pk')
        issue = Issue.objects.get(id=issue_id)

        # On récupère les contributeurs du projet
        contributor = Contributor.objects.filter(project=project, user=user).first()

        # Vérifier si l'utilisateur est un contributeur du projet
        if not contributor:
            raise ValidationError("You are not a contributor to this project.")

        # On sauvegarde l'issue en associant le projet
        issue = serializer.save(issue=issue, author=contributor)

    def get_permissions(self):
        return [IsAuthenticated(), IsContributorAuthenticated()]

