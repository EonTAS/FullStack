from django.shortcuts import render
from .forms import OrderForm
from django.shortcuts import render, redirect, reverse, get_object_or_404

from projects.models import Project 

# Create your views here.
def checkout(request, id):
    project = get_object_or_404(Project, pk=id)
    if not request.user.is_authenticated:                
        messages.error(request, "no search entered")
        return redirect(reverse('checkout'))

    if request.method == 'POST':
        order_form = OrderForm(data=request.POST)
        if order_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = OrderForm.save(commit=False)
            # Assign the current post to the comment
            new_comment.item = project
            new_comment.owner = request.user
            # Save the comment to the database
            new_comment.save()
    else:
        order_form = OrderForm()

    context = {
        'project': project,
        "order_form": order_form
    }
    return render(request, "checkout/checkout.html", context)