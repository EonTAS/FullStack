from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.all_projects, name="projects"),
    path('<id>', views.project_details, name="project_details"),
]
