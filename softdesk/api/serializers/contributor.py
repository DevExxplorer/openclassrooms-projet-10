from rest_framework import serializers

from api.models import Contributor, Project,  CustomUser

class ContributorSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = Contributor
        fields = '__all__'