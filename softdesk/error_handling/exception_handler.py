import logging

from rest_framework.views import exception_handler

from error_handling.errors import ERRORS

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
        Gestion des exceptions pour Django REST Framework.
        Remplace les messages par default de Django Rest par des messages personnalisés
        définis dans le dictionnaire ERRORS.

        :param exc: L’exception levée
        :param context: Contexte dans lequel l’exception a été levée
        :return: Réponse modifiée avec messages d'erreur personnalisés
    """
    response = exception_handler(exc, context)

    if response is not None:
        errors = response.data

        if isinstance(errors, dict):
            updated_errors = {}
            for field, error in errors.items():
                if field in ERRORS:
                    updated_errors[field] = [ERRORS[field]]
                else:
                    updated_errors[field] = error
            response.data = updated_errors
        else:
            logger.warning(f"Unexpected error format: {errors}")

    return response
