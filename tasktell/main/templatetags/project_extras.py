from django import template
from django.contrib.auth import get_user_model
from tasktell.main.models import Project, Member, Tasks
import datetime as dt

register = template.Library()
UserModel = get_user_model()


@register.simple_tag
def disable(project_pk, user_pk):
    try:
        Project.objects.filter(member__user_id=user_pk).get(pk=project_pk)
        return 'disabled'
    except Exception:
        return


@register.simple_tag
def progress(project_pk):
    completed = Tasks.objects.filter(project_id=project_pk, is_done=True)
    incomplete = Tasks.objects.filter(project_id=project_pk, is_done=False)
    if not (len(incomplete) + len(completed)):
        return 0
    if completed == incomplete:
        return 100
    completion = (len(completed)) / (len(completed) + len(incomplete)) * 100
    return f'{completion:.0f}'


@register.inclusion_tag('tags/project-nav-dropdown.html')
def list_projects(user_pk):
    list_projects = Project.objects.filter(member__user_id=user_pk)
    return {'list_projects': list_projects}


@register.simple_tag
def members_count(project):
    project_count = project.member_set.count()
    return project_count


@register.filter
def days_ago(value):
    return (dt.date.today() - value).days
