from rest_framework.views import exception_handler

from error_handling.errors import ERRORS


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        errors = response.data

        if isinstance(errors, dict):
            for field, error in errors.items():
                if field in ERRORS:
                    for e in error:
                        new_message = str(e).replace(e, ERRORS[field])
                        errors[field] = [new_message]
        else:
            print(errors)

    return response
