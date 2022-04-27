from functools import wraps

from django.http import HttpResponseNotAllowed
from django.utils.log import log_response

from tasktell.main.models import Member


def require_http_methods_mod_and_owner(request_method_set):
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            user_member = request.user.member_set.get(user_id=request.user.pk, projects=kwargs['pk'])
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
            user_member = request.user.member_set.get(user_id=request.user.pk, projects=kwargs['pk'])
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
