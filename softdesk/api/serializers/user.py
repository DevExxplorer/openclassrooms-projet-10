from rest_framework import serializers
from datetime import date

from api.models.user import CustomUser


class UserSerializer(serializers.HyperlinkedModelSerializer):
    birth_date = serializers.DateField(required=True)

    class Meta:
        model = CustomUser
        fields = [ 'id', 'username', 'first_name', 'last_name', 'email', 'birth_date', 'can_be_contacted', 'can_data_be_shared']

    def validate_birth_date(self, value):
        date_now = date.today()
        date_birthday = value

        if date_now.year - date_birthday.year >= 15:
            print(date_now.year)
            print(date_birthday.year)
        else:
            raise serializers.ValidationError('Trop jeune')

        return value