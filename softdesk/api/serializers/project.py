from rest_framework import serializers

from api.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    URL = 'http://127.0.0.1:8000/api/projects/'
    link = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields =  [ 'id', 'title', 'description', 'type_project', 'created_at', 'link']

    def get_link(self, obj):
        links = {
            'contributors': f'{self.URL}{obj.id}/contributors',
            'issues': f'{self.URL}{obj.id}/issues',
        }
        return links
