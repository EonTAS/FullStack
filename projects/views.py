from django.shortcuts import render, redirect, reverse, get_object_or_404, resolve_url
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Project, Category, Comment
from .forms import CommentForm, ProjectForm

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
        project_form = ProjectForm(data=request.POST)
        if project_form.is_valid():
            # Create Comment object but don't save to database yet
            project = project_form.save(costDistribution=costDistribution)
            # Assign the current post to the comment
            # Save the comment to the database
            if request.POST["action"] == "fund":
                return redirect(resolve_url('checkout',id=project.id))
            else:
                return redirect(resolve_url('project_details', id=project.id))


    else:
        project_form = ProjectForm()
    
    context = {
        "project_form": project_form,
        "costDistribution": costDistribution
    }

    return render(request, "projects/project_request.html", context)