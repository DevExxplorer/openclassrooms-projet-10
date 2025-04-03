from rest_framework import serializers

from api.models import Project
from api.serializers.contributor import ContributorSerializer


class ProjectSerializer(serializers.ModelSerializer):
    URL = 'http://127.0.0.1:8000/api/projects/'
    link = serializers.SerializerMethodField()
    contributors = ContributorSerializer(source="contributors_project", many=True, read_only=True)

    class Meta:
        model = Project
        fields =  [ 'id', 'title', 'description', 'type_project', 'created_at',  'contributors', 'link']

    def get_link(self, obj):
        links = {
            'contributors': f'{self.URL}{obj.id}/contributors',
            'issues': f'{self.URL}{obj.id}/issues',
        }
        return links
