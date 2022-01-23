from django.urls import path, include

from . import views
from .webhooks import webhook
urlpatterns = [
    path('<id>', views.checkout, name="checkout"),
    path('success/<order_number>', views.checkout_success, name="checkout_success"),
    path('cache_checkout/', views.cache_checkout_data, name="cache_checkout"),
    path('wh/', webhook, name="webhook"),
]
