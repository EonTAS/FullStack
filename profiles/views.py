from django.shortcuts import render
from projects.models import Project, Category, Comment
# Create your views here.
from django.shortcuts import render, redirect, reverse, get_object_or_404, resolve_url

from django.contrib.auth.decorators import login_required 

@login_required
def profile(request):
    orders = request.user.commission_set.all()
    
    #if request.method == 'POST':
    #    comment_form = CommentForm(data=request.POST)
    #    if comment_form.is_valid():
#
    #        # Create Comment object but don't save to database yet
    #        new_comment = comment_form.save(commit=False)
    #        # Assign the current post to the comment
    #        new_comment.item = project
    #        new_comment.owner = request.user
    #        # Save the comment to the database
    #        new_comment.save()
    #else:
    #    comment_form = CommentForm()

    #print(request.user.fields)
    context = {
        "user": request.user,
        "funded": orders
    }
    return render(request, "profiles/profile.html", context)
