from rest_framework import serializers
from api.models import Project, CustomUser
from api.serializers.contributor import ContributorSerializer


class ProjectSerializer(serializers.ModelSerializer):
    """
   Sérialiseur pour le modèle Project.
   """
    baseUrl = 'http://127.0.0.1:8000/'
    url = f'{baseUrl}api/projects/'
    link = serializers.SerializerMethodField()
    contributors = ContributorSerializer(source="contributors_project", many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.id')

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type_project', 'created_at', 'author', 'contributors', 'link']
        read_only_fields = ['author']

    def get_link(self, obj):
        links = {
            'contributors': f'{self.url}{obj.id}/contributors',
            'issues': f'{self.url}{obj.id}/issues',
        }
        return links
