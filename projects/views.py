from django.shortcuts import render
from .models import Project

# Create your views here.
def all_projects(request):
    projects = Project.objects.all()
    context = {
        'projects': projects
    }
    return render(request, "projects/projects.html", context)