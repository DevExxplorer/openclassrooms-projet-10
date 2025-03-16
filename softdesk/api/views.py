from rest_framework.viewsets import ReadOnlyModelViewSet

from api.models import CustomUser
from api.serializers.user import UserSerializer


class UserViewSet(ReadOnlyModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return CustomUser.objects.all().order_by('-date_joined')
