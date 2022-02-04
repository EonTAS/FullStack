from django.shortcuts import render
from projects.models import Project, Category, Comment
# Create your views here.
from django.shortcuts import render, redirect, reverse, get_object_or_404, resolve_url
from django.contrib import messages
from django.contrib.auth.decorators import login_required 

from django.db.models import DateField, ExpressionWrapper, F

from .forms import UserForm

#View users Profile
@login_required
def profile(request):
    #if user is editting their profile, save that here
    if request.method == 'POST':
        form = UserForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Data updated")
    else:
        form = UserForm(instance=request.user)

    #return list of all items funded by the user and all items suggested by the user to the 
    funded = request.user.commission_set.annotate(commItem__endDate=ExpressionWrapper(
            F('commItem__startDate') + F('commItem__expectedLength'), output_field=DateField())).all()
    suggested = request.user.project_set.annotate(endDate=ExpressionWrapper(
            F('startDate') + F('expectedLength'), output_field=DateField())).all()
    
    context = {
        "user": request.user,
        "funded": funded,
        "suggested":  suggested,
        "form": form
    }
    return render(request, "profiles/profile.html", context)
