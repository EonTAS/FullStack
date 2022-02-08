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

# view for when showing every project


def all_projects(request):
    projects = Project.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    # only display approved projects if not an admin
    if not request.user.is_superuser:
        projects = projects.filter(approved=True)

    if request.GET:
        # filter down to just the categorys specified
        if 'category' in request.GET:
            categories = request.GET["category"].split(",")
            projects = projects.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        # if some sorting information added, filter as appropriate
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "no search entered")
                return redirect(reverse('projects'))
            queries = Q(name__icontains=query) | Q(
                description__icontains=query)
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
                # reverse order if the direction is descending instead of ascending
                if direction == 'desc':
                    sortkey = "-" + sortkey
            else:
                direction = "asc"
            projects = projects.order_by(sortkey)

    # list of sortings to fill in the dropdown list with instead of having on the page
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
    # add sorting by approved for admins to allow easier approving
    if request.user.is_superuser:
        possibleSortings += [
            {"name": "approved_asc", "friendlyName": "Unapproved first"},
            {"name": "approved_desc", "friendlyName": "Approved first"},
        ]

    # add an enddate field to display for user on the site
    projects = projects.annotate(endDate=ExpressionWrapper(
        F('startDate') + F('expectedLength'), output_field=DateField()))

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
        # if the form submitted was a comment, handle that
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
        # if the form submitted was an update and wasnt somehow spoofed by a regular user, handle that
        elif "updateForm" in request.POST and request.user.is_superuser:
            update_form = UpdateForm(data=request.POST)
            if update_form.is_valid():
                # Create update object but don't save to database yet
                update = update_form.save(commit=False)
                update.item = project
                # Save the update to the database
                update.save()
    # only send form if its a user
    if request.user.is_superuser:
        update_form = UpdateForm()
    # always create a new comment so it doesnt re-suggest same one
    comment_form = CommentForm()

    context = {
        'project': project,
        'comments': comments,
        "comment_form": comment_form,
        "update_form": update_form
    }
    if project.startDate:  # calc an enddate if a startdate specified
        context["projectEndDate"] = project.startDate + project.expectedLength

    return render(request, "projects/project_details.html", context)


def project_request(request):
    # only allow users who are logged in to submit a request
    if not request.user.is_authenticated:
        messages.error(request, "please login before suggesting a project")
        return redirect(reverse('account_login'))

    project_form = None
    # suggested cost layout of category + timeframe
    costDistribution = {}
    for category in Category.objects.all():
        costDistribution["shortterm" + str(category.id)] = float(category.examplePrice_shortterm)
        costDistribution["mediumterm" + str(category.id)] = float(category.examplePrice_midterm)
        costDistribution["longterm" + str(category.id)] = float(category.examplePrice_longterm)
    
    if request.method == 'POST':
        project_form = ProjectSuggestForm(request.POST, request.FILES)
        if project_form.is_valid():
            # Create Comment object but don't save to database yet
            project = project_form.save(
                costDistribution=costDistribution, suggester=request.user)

            messages.success(
                request, "Project idea submitted, you will recieve an email when it is approved for purchase")
            return redirect('projects')
    else:
        project_form = ProjectSuggestForm()

    context = {
        "project_form": project_form,
        "costDistribution": costDistribution
    }

    return render(request, "projects/project_request.html", context)


@staff_member_required
def add_project(request):
    # if post request, add project to database
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save()
            messages.success(request, 'Successfully added item!')
            return redirect(reverse('project_detail', args=[item.id]))
        else:
            messages.error(
                request, 'Failed to add item. Please ensure the form is valid.')
    else:
        form = ProjectForm()

    context = {
        'form': form,
    }

    return render(request, 'projects/add_project.html', context)


@staff_member_required
def edit_project(request, id):
    # project to be editted has primary key of id
    project = get_object_or_404(Project, pk=id)

    if request.method == 'POST':
        # save current state of project so that when its editted changes can easily be detected
        prevState = copy(project)
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()

            body = "Your project has been approved and can now be funded at $asdf\nAdditional changes found below:\n"

            newState = project
            changesString = ""
            # iterate through each field in the project and detect if it was changed by the edit, detail it here
            for key in Project._meta.fields:
                name = key.name
                if name != "approved":  # dont detect approved changed since thats listed seperate
                    if getattr(newState, name) != getattr(prevState, name):
                        changesString += f'  {key.verbose_name.capitalize()} changed from "{getattr(prevState, name)}" to "{getattr(newState, name)}"\n'
            body = ""
            header = "Project Changed"
            if prevState.approved != project.approved:
                if project.approved == True:
                    body = "Project has been approved and can now be funded at $asdf\n"
                    header = "Project Approved!"
                else:
                    body = "Project has been unapproved and can no longer be funded until reapproved\n"
            else:
                body = "Project has changed\n"
            # if project has detected changes, add to body
            if changesString != "":
                body += "Changes to project can be found below:\n"
                body += changesString
            # create an update object with the changes, which automatically sends email to relevant users
            a = Update(item=project, header=header, body=body)
            a.save()

            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('project_details', args=[project.id]))
        else:
            messages.error(
                request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProjectForm(instance=project)
        messages.info(request, f'You are editing {project.name}')

    context = {
        'form': form,
        'project': project,
    }

    return render(request, 'projects/edit_project.html', context)


@staff_member_required
def delete_project(request, id):
    # delete project specified by id
    item = get_object_or_404(Project, pk=id)
    item.delete()
    messages.success(request, 'Item deleted!')
    return redirect(reverse('projects'))


@staff_member_required
def delete_comment(request, projectId, commentId):
    # delete comment on project specified by ids
    project = get_object_or_404(Project, pk=projectId)
    project.comment_set.get(pk=commentId).delete()
    messages.success(request, 'Comment deleted!')
    return redirect(resolve_url("project_details", id=projectId))
