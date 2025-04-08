from rest_framework import serializers

from api.models import Contributor, Project,  CustomUser
from api.serializers.user import UserSerializer


class ContributorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Contributor
        fields = ['user']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation['user']