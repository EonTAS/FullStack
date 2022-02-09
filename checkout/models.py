
import uuid

from django.db import models
from django.conf import settings

from projects.models import Project, Update

from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta


class Commission(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)

    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)

    date = models.DateTimeField(auto_now_add=True)

    order_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    # there can only be one payment per item, so one to one field
    commItem = models.OneToOneField(
        Project, null=True, blank=False, on_delete=models.SET_NULL)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             null=True, on_delete=models.SET_NULL)

    stripe_pid = models.CharField(
        unique=True, max_length=254, null=False, blank=False, default='')
    # create order uuid so its not easily guessable

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            print("hi")
            self.order_number = self._generate_order_number()
            print(len(self.order_number))
        # copy price over from commission item
        self.order_price = self.commItem.price

        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.commItem) + " " + self.order_number

# detect when a payment is made and create an update for it


@receiver(post_save, sender=Commission)
def sendUpdate(sender, instance, created, **kwargs):
    if created:
        if not instance.commItem.startDate:
            # set startdate of a now paid for item to 1 week after the payment
            instance.commItem.startDate = datetime.now() + timedelta(days=7)
            instance.commItem.save()
        header = f'Project {instance.commItem} funded for £{instance.order_price}'
        body = f"Thank you {instance.user} for funding {instance.commItem}. We will begin working on this project on {instance.commItem.startDate.strftime('%d-%m-%Y')}."
        Update.objects.create(item=instance.commItem, header=header, body=body)
