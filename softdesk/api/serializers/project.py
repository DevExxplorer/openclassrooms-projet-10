from rest_framework import serializers
from api.models import Project
from api.serializers.contributor import ContributorSerializer


class ProjectSerializer(serializers.ModelSerializer):
    """
   Sérialiseur pour le modèle Project.
   """
    contributors = ContributorSerializer(source="contributors_project", many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.id')

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type_project', 'created_at', 'author', 'contributors']
        read_only_fields = ['author']
