from rest_framework.permissions import BasePermission


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
    Autorise uniquement les utilisateurs qui sont contributeurs du projet.
    """

    def has_permission(self, request, view):
        # Assurez-vous que l'utilisateur est connecté
        if not (request.user and request.user.is_authenticated):
            return False

