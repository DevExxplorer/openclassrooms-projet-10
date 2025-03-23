from rest_framework import serializers

from api.models.user import CustomUser


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CustomUser
        fields = [ 'id', 'username', 'first_name', 'last_name', 'email', 'birth_date', 'can_be_contacted', 'can_data_be_shared']

    def validate(self, data):
        if data.get('is_superuser', False):
            data['birth_date'] = None
        else:
            if 'birth_date' not in data or data['birth_date'] is None:
                raise serializers.ValidationError({'birth_date': 'Ce champ est obligatoire.'})
            else:
                data['birth_date'] = data['birth_date']

        return data