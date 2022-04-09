from django.urls import path
from django.views.generic import TemplateView
from tasktell.main.views.project import ProjectCreateView, PublicProjectsListView, ProjectDetailsView


urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('create-project/', ProjectCreateView.as_view(), name='create project'),
    path('public-projects/', PublicProjectsListView.as_view(), name='public projects'),
    path('project-details/<int:pk>/', ProjectDetailsView.as_view(), name='project details'),
]
