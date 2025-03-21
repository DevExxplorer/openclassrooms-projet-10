from rest_framework import serializers

from api.models.user import CustomUser


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'birth_date', 'can_be_contacted', 'can_data_be_shared']
