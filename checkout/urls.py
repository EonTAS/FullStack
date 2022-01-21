from django.urls import path, include

from . import views

urlpatterns = [
    path('<id>', views.checkout, name="checkout"),
]
