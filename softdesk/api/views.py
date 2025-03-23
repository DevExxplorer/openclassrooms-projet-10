from rest_framework.viewsets import ModelViewSet

from api.models import CustomUser, Project, Issue

from api.serializers.user import UserSerializer
from api.serializers.project import ProjectSerializer
from api.serializers.issue import IssueSerializer

class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return CustomUser.objects.all().order_by('-date_joined')


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.all()


class IssueViewSet(ModelViewSet):
    serializer_class = IssueSerializer
    
    def get_queryset(self):
        return Issue.objects.all()