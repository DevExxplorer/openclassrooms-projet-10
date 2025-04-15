from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from api.models import Contributor, Project


class IsAuthor(BasePermission):
    """
    Permission pour vérifier que l'utilisateur est l'auteur du projet
    """

    def has_permission(self, request, view):
        """
        Vérifie que l'auteur id et l'id de l'utilisateur connecté soit les mêmes
        """
        project_id = view.kwargs.get('project_pk')
        project = Project.objects.get(id=project_id)

        print('TEST',project.author.user, request.user )
        if project.author.user != request.user:
            raise PermissionDenied("Vous devez être l'auteur du projet pour effectuer cette action.")

        return  True

    def has_object_permission(self, request, view, obj):
        """
        Vérifie que l'auteur id et l'id de l'utilisateur connecté soit les mêmes
        """
        print('test 1', self)
        print('test 2', request)
        print('test 3', view)
        print('test 4', obj)

        return True


class IsContributorAuthenticated(BasePermission):
    """
    Permission pour vérifier que l'utilisateur est contributeur du projet.
    """
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'contributors'):
            return obj.contributors.filter(user=request.user).exists()
        return Contributor.objects.filter(user=request.user, project=obj.project).exists()

class DenyAll(BasePermission):
    """
    Bloque l'acces à certains enpoints
    """
    def has_permission(self, request, view):
        pass

    def has_object_permission(self, request, view, obj):
       pass