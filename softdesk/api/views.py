# from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.models import CustomUser, Project, Issue, Contributor

from api.serializers.user import UserSerializer
from api.serializers.project import ProjectSerializer
from api.serializers.issue import IssueSerializer
from api.serializers.contributor import ContributorSerializer

class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return CustomUser.objects.all().order_by('-date_joined')


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.all()


class IssueViewSet(ModelViewSet):
    serializer_class = IssueSerializer
    
    def get_queryset(self):
        return Issue.objects.all()


class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorSerializer

    def get_queryset(self):
        project_id = self.kwargs.get('project_pk')
        return Contributor.objects.filter(project_id=project_id)

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_pk')
        project = Project.objects.get(id=project_id)
        serializer.save(project=project)