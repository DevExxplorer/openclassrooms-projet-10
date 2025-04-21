from rest_framework import serializers
from api.models import Contributor


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['user']

    def to_representation(self, instance):
        """Retourne uniquement l'identifiant et l'username de l'utilisateur"""
        user = instance.user

        return {
            "id_contributor": instance.id,
            "user": {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            }
        }
