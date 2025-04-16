from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from api.models import Contributor, Project


class IsAuthor(BasePermission):
    """
    def has_permission(self, request, view):
        print('HAS_PERMISSION isauthor')
        project_id = view.kwargs.get('project_pk') or view.kwargs.get('pk')
        project = Project.objects.get(id=project_id)

        if project.author.user != request.user:
            raise PermissionDenied("Vous devez être l'auteur du projet pour effectuer cette action.")

        return  True
    """
    
    def has_object_permission(self, request, view, obj):
        print('HAS_OBJ_PERMISSION isauthor')
        return True


class IsProjectContributor(BasePermission):

    def has_permission(self, request, view):
        print('HAS_PERMISSION PROJECT_CONTRIBUTOR')
        project_id = view.kwargs.get('project_pk') or view.kwargs.get('pk')
        project = Project.objects.get(pk=project_id)

        is_contributor = project.contributors_project.filter(user=request.user).exists()

        if is_contributor:
            return True

        raise PermissionDenied("Vous n'êtes pas contributeur du projet.")

    def has_object_permission(self, request, view, obj):
        print('HAS_OBJECT_PERMISSION PROJECT_CONTRIBUTOR')

        if  hasattr(obj, 'contributors_project'):
            is_contributor = obj.contributors_project.filter(user=request.user).exists()
        else:
            project_id = view.kwargs.get('project_pk') or view.kwargs.get('pk')
            project = Project.objects.get(pk=project_id)

            is_contributor = project.contributors_project.filter(user=request.user).exists()

        if is_contributor:
            return True

        raise PermissionDenied("Vous n'êtes pas contributeur du projet.")


class IsSelf(BasePermission):
    """
    Autorise un utilisateur à accéder ou modifier uniquement son propre profil utilisateur.
    """
    def has_object_permission(self, request, view, obj):
        """
        Vérifie que l'utilisateur authentifié tente d'accéder uniquement à son propre objet
        """
        return obj == request.user

    def has_permission(self, request, view):
        """
        Bloque l'acces à l'endpoint GET /users/ ou DELETE /users/
        """
        if view.action == 'list' or view.action == 'destroy':
            return True # Passer à False pour desactiver GET /users/
        return True
