from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Project, Category, Comment

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
    comments = Comment.objects.all()
    comments.filter(item=project)
    print(comments)
    context = {
        'project': project,
        'comments': comments
    }
    return render(request, "projects/project_details.html", context)