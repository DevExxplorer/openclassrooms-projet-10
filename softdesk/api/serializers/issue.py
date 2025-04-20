from rest_framework import serializers
from api.models import Issue


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'status', 'priority', 'author', 'type_issue', 'created_at']
        read_only_fields = ['author']
