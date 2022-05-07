from django.urls import path
from django.views.generic import TemplateView

from tasktell.main.views.member import InviteMemberView, AcceptInviteView, LeaveTeamView, RemoveFromTeamView, \
    ChangeRoleView
from tasktell.main.views.project import ProjectCreateView, PublicProjectsListView, ProjectDetailsView
from tasktell.main.views.task import TaskEditView, TaskDeleteView, TaskCompleteView
from tasktell.main.views.task_list import TaskListDeleteView

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('create-project/', ProjectCreateView.as_view(), name='create project'),
    path('public-projects/', PublicProjectsListView.as_view(), name='public projects'),
    path('project-details/<int:pk>/', ProjectDetailsView.as_view(), name='project details'),
    path('project-edit-tasks/<int:pk>/', TaskEditView.as_view(), name='edit task'),
    path('project-delete-tasks/<int:pk>/', TaskDeleteView.as_view(), name='delete task'),
    path('project-complete-tasks/<int:pk>/<int:id>/', TaskCompleteView.as_view(), name='complete task'),
    path('project-delete-task-list/<int:pk>/', TaskListDeleteView.as_view(), name='delete taskboard'),
    path('invite-member/<int:pk>/', InviteMemberView.as_view(), name='invite member'),
    path('accept-invite/<int:pk>/', AcceptInviteView.as_view(), name='accept invite'),
    path('leave-team/<int:pk>/', LeaveTeamView.as_view(), name='leave team'),
    path('remove-from-team/<int:pk>/<int:id>/', RemoveFromTeamView.as_view(), name='remove from team'),
    path('change-role/<int:pk>/<int:id>/', ChangeRoleView.as_view(), name='change role'),
]
