from django.shortcuts import render
from projects.models import Project, Category, Comment
# Create your views here.
from django.shortcuts import render, redirect, reverse, get_object_or_404, resolve_url

from django.contrib.auth.decorators import login_required 

@login_required
def profile(request):
    orders = request.user.commission_set.all()
    
    context = {
        "user": request.user,
        "funded": orders
    }
    return render(request, "profiles/profile.html", context)

def fundedProjects(request):
    if not request.user.is_authenticated:
        return redirect("home")
    funded = request.user.commission_set.all()
    funded_projects = [commission.commItem for commission in funded]

    context = {
        'projects': funded_projects,
    }
    return render(request, "projects/projects_funded.html", context)