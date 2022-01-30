from django.shortcuts import render, redirect, reverse, get_object_or_404, resolve_url
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Project, Category, Comment
from .forms import CommentForm, ProjectSuggestForm, ProjectForm

from django.contrib.admin.views.decorators import staff_member_required


# Create your views here.
def all_projects(request):
    projects = Project.objects.all()
    query = None
    categories = None
    sort = None
    direction = None 
    if request.GET:
        if 'category' in request.GET:
            categories = request.GET["category"].split(",")
            projects = projects.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "no search entered")
                return redirect(reverse('projects'))
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            projects = projects.filter(queries)
        
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey 
            if sortkey == 'name':
                sortkey = "lower_name"
                projects = projects.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = "-" + sortkey
            else:
                direction = "asc"
            projects = projects.order_by(sortkey)

    possibleSortings = [
        {"name": "reset", "friendlyName": "Sort by."},
        {"name": "price_asc", "friendlyName": "Price (low to high)"},
        {"name": "price_desc", "friendlyName": "Price (high to low)"},
        {"name": "name_asc", "friendlyName": "Name (A-Z)"},
        {"name": "name_desc", "friendlyName": "Name (Z-A)"},
        {"name": "category_asc", "friendlyName": "Category (A-Z)"},
        {"name": "category_desc", "friendlyName": "Category (Z-A)"},
    ]

    context = {
        'projects': projects,
        'search': query,
        'categories': categories,
        'sorting': f'{sort}_{direction}',
        'possibleSortings': possibleSortings
    }
    return render(request, "projects/projects.html", context)

def project_details(request, id):
    project = get_object_or_404(Project, pk=id)
    comments = project.comment_set.all()


    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.item = project
            new_comment.owner = request.user
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    context = {
        'project': project,
        'comments': comments,
        "comment_form": comment_form
    }
    return render(request, "projects/project_details.html", context)


def project_request(request):
        
    if not request.user.is_authenticated:                
        messages.error(request, "please login before suggesting a project")
        return redirect(reverse('account_login'))

    project_form = None
    costDistribution = {
        "shortterm Codes and Mods": 20,
        "mediumterm Codes and Mods": 30,
        "longterm Codes and Mods": 40,
        "shortterm Art": 15,
        "mediumterm Art": 25,
        "longterm Art": 35,
        "shortterm Miscellaneous": 10,
        "mediumterm Miscellaneous": 20,
        "longterm Miscellaneous": 25,
    }
    if request.method == 'POST':
        project_form = ProjectSuggestForm(request.POST, request.FILES)
        if project_form.is_valid():
            # Create Comment object but don't save to database yet
            project = project_form.save(costDistribution=costDistribution, suggester=request.user)
            # Assign the current post to the comment
            # Save the comment to the database
            if request.POST["action"] == "fund":
                return redirect(resolve_url('checkout',id=project.id))
            else:
                return redirect(resolve_url('project_details', id=project.id))
    else:
        project_form = ProjectSuggestForm()
    
    context = {
        "project_form": project_form,
        "costDistribution": costDistribution
    }

    return render(request, "projects/project_request.html", context)

@staff_member_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save()
            messages.success(request, 'Successfully added item!')
            return redirect(reverse('project_detail', args=[item.id]))
        else:
            messages.error(request, 'Failed to add item. Please ensure the form is valid.')
    else:
       form = ProjectForm()
    template = 'projects/add_project.html'
    context = {
        'form': form,
    }

    return render(request, template, context)

@staff_member_required
def edit_project(request, id):
    project = get_object_or_404(Project, pk=id)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('project_details', args=[project.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProjectForm(instance=project)
        messages.info(request, f'You are editing {project.name}')
#
    template = 'projects/edit_project.html'
    context = {
        'form': form,
        'project': project,
    }

    return render(request, template, context)

@staff_member_required
def delete_project(request, id):
    item = get_object_or_404(Project, pk=id)
    item.delete()
    messages.success(request, 'Item deleted!')
    return redirect(reverse('projects'))
