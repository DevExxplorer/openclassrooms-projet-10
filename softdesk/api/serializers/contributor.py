from rest_framework import serializers

from api.models import Contributor, Project,  CustomUser

class ContributorSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(), required=False, write_only=True, allow_null=True, default=None
    )
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = Contributor
        fields = '__all__'