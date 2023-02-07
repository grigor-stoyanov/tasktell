from functools import wraps

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotAllowed
from django.utils.log import log_response

from tasktell.common.helpers import get_logged_in_user_as_member_or_none
from tasktell.main.models import Member, Project


def require_http_methods_mod_and_owner(request_method_set):
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            user_member = get_logged_in_user_as_member_or_none(kwargs['pk'], request.user.pk)
            if user_member:
                if user_member.role == Member.Roles.OWNER or user_member.role == Member.Roles.MOD:
                    request_method_set.add('POST')
            if request.method not in request_method_set:
                response = HttpResponseNotAllowed(request_method_set)
                log_response(
                    'Method Not Allowed (%s): %s', request.method, request.path,
                    response=response,
                    request=request,
                )
                return response
            return func(request, *args, **kwargs)

        return inner

    return decorator


def require_http_methods_owner(request_method_set):
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            user_member = get_logged_in_user_as_member_or_none(kwargs['pk'], request.user.pk)
            if user_member:
                if user_member.role == Member.Roles.OWNER:
                    request_method_set.add('POST')
            if request.method not in request_method_set:
                response = HttpResponseNotAllowed(request_method_set)
                log_response(
                    'Method Not Allowed (%s): %s', request.method, request.path,
                    response=response,
                    request=request,
                )
                return response
            return func(request, *args, **kwargs)

        return inner

    return decorator
