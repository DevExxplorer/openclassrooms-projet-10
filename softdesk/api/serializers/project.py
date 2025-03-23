from rest_framework import serializers

from api.models import Project, CustomUser

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'
