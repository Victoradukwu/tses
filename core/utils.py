from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, PermissionDenied
from rest_framework.response import Response


def custom_exception_handler(exc, context):

    msg = exc.detail if hasattr(exc, 'detail') else str(exc)
    if type(exc) in [NotAuthenticated, PermissionDenied, AuthenticationFailed]:
        status = 403
    elif type(exc) in [ObjectDoesNotExist, Http404]:
        status = 404
    else:
        status = 400

    return Response({'detail': msg}, status=status)