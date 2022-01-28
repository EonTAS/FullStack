from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.all_projects, name="projects"),
    path('view/<id>', views.project_details, name="project_details"),
    path('request', views.project_request, name="project_request"),
    path('funded', views.projects_funded, name="projects_funded")
]
