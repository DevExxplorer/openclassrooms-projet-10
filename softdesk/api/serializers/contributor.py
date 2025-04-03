from rest_framework import serializers

from api.models import Contributor, Project,  CustomUser
from api.serializers.user import UserSerializer


class ContributorSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(), required=False, write_only=True, allow_null=True, default=None
    )
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), write_only=True, source="user"
    )


    class Meta:
        model = Contributor
        fields = ['id', 'project', 'user', 'user_id']