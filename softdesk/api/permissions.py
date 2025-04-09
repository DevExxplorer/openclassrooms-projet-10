from rest_framework.permissions import BasePermission
from api.models import Contributor


class IsAuthorAuthenticated(BasePermission):
    """
    Autorise uniquement l'auteur du projet.
    """

    def has_permission(self, request, view):
        # Assurez-vous que l'utilisateur est connecté
        if not (request.user and request.user.is_authenticated):
            return False


class IsContributorAuthenticated(BasePermission):
    """
    Autorise uniquement les contributeurs du projet.
    """

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        project_id = view.kwargs.get('project_pk') or view.kwargs.get('pk')
        if not project_id:
            return False

        return Contributor.objects.filter(project_id=project_id, user=user).exists()
