from django.core.exceptions import ObjectDoesNotExist

from tasktell.main.models import Project


def get_logged_in_user_as_member_or_none(project_pk, user_pk):
    try:
        return Project.objects.get(pk=project_pk).member_set.get(user_id=user_pk)
    except ObjectDoesNotExist:
        return None
