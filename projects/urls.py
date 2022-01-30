from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.all_projects, name="projects"),
    path('view/<id>', views.project_details, name="project_details"),
    path('request', views.project_request, name="project_request"),
    path('add', views.add_project, name="add_project"),
    path('edit/<id>', views.edit_project, name="edit_project"),
    path('delete/<id>', views.delete_project, name="delete_project")
]
