from rest_framework import serializers
from datetime import date
from api.models.user import CustomUser


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the user model
    """
    birth_date = serializers.DateField(
        required=True,
        input_formats=['%d-%m-%Y'],
        format='%d-%m-%Y'
    )
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'password', 'email', 'birth_date', 'can_be_contacted', 'can_data_be_shared']

    @staticmethod
    def validate_birth_date(value):
        """
        Validation personnalisée pour s'assurer que l'utilisateur est au moins 15 ans.
        """
        date_now = date.today()
        date_birthday = value

        if date_now.year - date_birthday.year <= 15:
            raise serializers.ValidationError('Oups ! Tu dois avoir au moins 15 ans pour accéder à cette fonctionnalité. Reviens quand tu auras l\'âge requis !')

        return value

    def create(self, validated_data):
        """
        Création d'un nouvel utilisateur en hachant le mot de passe.
        """
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
