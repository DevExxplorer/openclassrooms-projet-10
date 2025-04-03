from rest_framework import serializers

from api.models import Issue
from api.serializers.contributor import ContributorSerializer


class IssueSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()
    contributors = ContributorSerializer(source="project.contributors_project", many=True, read_only=True)

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'status', 'priority', 'author', 'type_issue',  'created_at', 'contributors', 'link']

    @staticmethod
    def get_link(obj):
        url = 'http://127.0.0.1:8000/api/projects/'
        base_url = f'{url}{obj.project.id}/issues/'
        links = f'{base_url}{obj.id}/comments/'
        return links