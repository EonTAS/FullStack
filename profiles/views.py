from django.shortcuts import render
from projects.models import Project, Category, Comment
# Create your views here.
from django.shortcuts import render, redirect, reverse, get_object_or_404, resolve_url
from django.contrib import messages
from django.contrib.auth.decorators import login_required 

from .forms import UserForm

@login_required
def profile(request):
    orders = request.user.commission_set.all()
    if request.method == 'POST':
        form = UserForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated")
    else:
        form = UserForm(instance=request.user)

    context = {
        "user": request.user,
        "funded": orders,
        "form": form
    }
    return render(request, "profiles/profile.html", context)
