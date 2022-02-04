
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

    order_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    commItem = models.OneToOneField(Project, null=True, blank=False, on_delete=models.SET_NULL)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, on_delete=models.SET_NULL)

    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')

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
            self.order_number = self._generate_order_number()
        self.order_price = self.commItem.price
        #self.commItem.payed_for = True 
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number

@receiver(post_save, sender=Commission)
def sendUpdate(sender, instance, created, **kwargs):
    if created:
        if not instance.commItem.startDate:
            instance.commItem.startDate = datetime.now() + timedelta(days=7)
            instance.commItem.save()
        header = f'Project {instance.commItem} funded for £{instance.order_price}'
        body = f"Thank you {instance.user} for funding {instance.commItem}. We will begin working on this project on {instance.commItem.startDate.strftime('%d-%m-%Y')}."
        Update.objects.create(project=instance.commItem, header=header, body=body)
        