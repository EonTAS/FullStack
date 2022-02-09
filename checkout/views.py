from django.shortcuts import render
from .forms import OrderForm
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.http import require_POST

from projects.models import Project
from .models import Commission

import stripe


@require_POST
def cache_checkout_data(request):
    # workaround to add metadata to the payment intent since you cant do that within the javascript
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'user': request.user.id,
            'item': request.POST.get('item')
        })
        print(stripe.PaymentIntent)
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(
            request, 'sorry your payment failed to go through, please try again later')
        return HttpResponse(content=e, status=400)


def checkout(request, id):
    # checkout is specific to individual items, handle that here
    project = get_object_or_404(Project, pk=id)
    # if a project has a commission already, that has been funded so shout at user
    if hasattr(project, 'commission'):
        messages.error(request, "item already funded")
        return redirect(reverse('home'))

    if project.approved == False:  # project cant be funded if not yet approved
        messages.error(request, 'item not yet approved')
        return redirect(reverse('home'))

    if not request.user.is_authenticated:  # must log in to fund item
        messages.error(request, "please login before trying to fund a project")
        return redirect(reverse('log_in'))

    # stripe setup
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    final_price = round(project.price * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=final_price,
        currency=settings.STRIPE_CURRENCY
    )
    order_form = None

    if request.method == 'POST':
        order_form = OrderForm(data=request.POST)
        pid = request.POST.get('client_secret').split('_secret')[0]
        if order_form.is_valid():
            # fill in order with all the other stuff the form doesnt contain
            order = order_form.save(commit=False)
            order.commItem = project
            order.user = request.user
            order.order_price = round(project.price * 100)
            order.stripe_pid = pid
            try:
                order.save()
            except IntegrityError as e: 
                if not 'unique constraint' in e.args[0]:
                    raise e
            finally:
                return redirect(reverse('checkout_success', args=[order.order_number]))
        messages.error(request, "There was an error with your form.")
    else:
        order_form = OrderForm()

    context = {
        'project': project,
        "order_form": order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }
    
    if project.startDate:  # calc an enddate if a startdate specified
        context["projectEndDate"] = project.startDate + project.expectedLength
    return render(request, "checkout/checkout.html", context)


def checkout_success(request, order_number):
    # once payment is made, send to this page
    order = get_object_or_404(Commission, order_number=order_number)
    messages.success(request, f'Order successfully processed! \
        your order number is {order_number} A confirmation email will be sent to {order.email}')

    context = {
        'order': order,
        'project': order.commItem
    }
    
    if project.startDate:  # calc an enddate if a startdate specified
        context["projectEndDate"] = project.startDate + project.expectedLength
        
    return render(request, "checkout/checkout_success.html", context)
