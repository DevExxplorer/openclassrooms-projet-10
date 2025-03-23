from rest_framework import serializers

from api.models import Issue

class IssueSerializer(serializers.ModelSerializer):
    # projects = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'status', 'priority', 'author', 'type_issue',  'created_at']

    # def get_projects(self, instance):
    #     queryset = instance.products.all()
    #     serializer = ProjeProjectSerializer(queryset, many=True)
    #     return serializer.data