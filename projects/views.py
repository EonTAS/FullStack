from django.shortcuts import render, redirect, reverse, get_object_or_404, resolve_url
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Project, Category, Comment, Update
from .forms import CommentForm, ProjectSuggestForm, ProjectForm, UpdateForm

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import DateField, ExpressionWrapper, F
from datetime import timedelta

from copy import copy

# Create your views here.
def all_projects(request):
    projects = Project.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if not request.user.is_superuser:
        projects = projects.filter(approved=True)
    projects = projects.annotate(endDate=ExpressionWrapper(
        F('startDate') + F('expectedLength'), output_field=DateField()))
    

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
        {"name": "commission_asc", "friendlyName": "Not funded first"},
        {"name": "commission_desc", "friendlyName": "funded first"},
    ]
    if request.user.is_superuser:
        possibleSortings += [
            {"name": "approved_asc", "friendlyName": "Unapproved first"},
            {"name": "approved_desc", "friendlyName": "Approved first"},
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
    update_form = None
    if request.method == 'POST':
        if "commentForm" in request.POST:
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():

                # Create Comment object but don't save to database yet
                new_comment = comment_form.save(commit=False)
                # Assign the current post to the comment
                new_comment.item = project
                new_comment.owner = request.user
                # Save the comment to the database
                new_comment.save()
        elif "updateForm" in request.POST and request.user.is_superuser:
            update_form = UpdateForm(data=request.POST)
            if update_form.is_valid():
                # Create Comment object but don't save to database yet
                update = update_form.save(commit=False)
                update.item = project
                # Save the comment to the database
                update.save()
    if request.user.is_superuser:
        update_form = UpdateForm()
    
    comment_form = CommentForm()

    context = {
        'project': project,
        'comments': comments,
        "comment_form": comment_form,
        "update_form": update_form
    }
    if project.startDate:
        context["projectEndDate"] = project.startDate + project.expectedLength

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
        prevState = copy(project)
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()

            body = "Your project has been approved and can now be funded at $asdf\nAdditional changes found below:\n"

            newState = project
            changesString = ""
            for key in Project._meta.fields:
                name = key.name
                if name != "approved":
                    if getattr(newState, name) != getattr(prevState, name):
                        changesString += f'  {key.verbose_name.capitalize()} changed from "{getattr(prevState, name)}" to "{getattr(newState, name)}"\n'
            body = ""
            header = "Project Changed"
            if prevState.approved != project.approved:
                if project.approved == True:
                    body = "Project has been approved and can now be funded at $asdf\n"
                    header = "Project Approved!"
                else:
                    body = "Your project has been unapproved and can no longer be funded until reapproved\n"
            else:
                body = "Your project has changed\n"
            if changesString != "":
                body += "Changes to project can be found below:\n"
                body += changesString
            a = Update(project=project, header=header, body=body)
            a.save()

            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('project_details', args=[project.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProjectForm(instance=project)
        messages.info(request, f'You are editing {project.name}')
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
    
@staff_member_required
def delete_comment(request, projectId, commentId):
    project = get_object_or_404(Project, pk=projectId)
    project.comment_set.get(pk=commentId).delete()
    messages.success(request, 'Comment deleted!')
    return redirect(resolve_url("project_details", id=projectId))
