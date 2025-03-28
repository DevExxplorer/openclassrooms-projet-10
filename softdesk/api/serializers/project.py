from rest_framework import serializers

from api.models import Project
from api.serializers.contributor import ContributorSerializer


class ProjectSerializer(serializers.ModelSerializer):
    contributors = ContributorSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'
