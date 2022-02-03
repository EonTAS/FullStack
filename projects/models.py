from django.db import models
from django.conf import settings


from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.mail import send_mail

from django.core.exceptions import ObjectDoesNotExist

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.friendly_name


class Project(models.Model):
    category = models.ForeignKey('Category', on_delete=models.PROTECT)

    name = models.CharField(max_length=254)
    description = models.TextField()

    price = models.DecimalField(max_digits=6, decimal_places=2)

    expectedLength = models.DurationField(
        verbose_name="Expected Development Time")
    startDate = models.DateField(
        null=True, blank=True, verbose_name="Start Date")

    approved = models.BooleanField(default=False)

    image = models.ImageField(null=True, blank=True,
                              upload_to="media/submitted")

    suggester = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Comment(models.Model):
    item = models.ForeignKey('Project', null=True,
                             blank=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              null=True, blank=True, on_delete=models.SET_NULL)
    header = models.CharField(max_length=30)
    body = models.TextField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'Comment "{self.body}" by {self.owner}'


class Update(models.Model):  # associated with account, account views all they have funded + able to see updates specifically for those ones in a special view
    project = models.ForeignKey(
        'Project', null=True, blank=True, on_delete=models.SET_NULL)

    header = models.CharField(max_length=30)
    body = models.TextField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'{self.project} update {self.created_on}'


@receiver(post_save, sender=Update)
def sendUpdate(sender, instance, created, **kwargs):
    if created:
        suggester = instance.project.suggester
        try:
            funder = instance.project.commission.user
        except ObjectDoesNotExist as e:
            funder = None

        if suggester == funder:
            if suggester.userprofile.email_updates:
                send_mail(
                    f'Hi {suggester} : New update for suggested and funded project {instance.project} - {instance.header}',
                    instance.body,
                    settings.DEFAULT_FROM_EMAIL,
                    [{suggester.email}],
                    fail_silently=False,
                )
        else:
            if suggester.userprofile.email_updates:
                send_mail(
                    f'Hi {suggester} : New update for suggested idea {instance.project} - {instance.header}',
                    instance.body + "\n\nIf you have any issue, please respond to this email and we will get back to you (not really this is a fake email)",
                    settings.DEFAULT_FROM_EMAIL,
                    [{suggester.email}],
                    fail_silently=False,
                )
            if funder and funder.userprofile.email_updates:
                send_mail(
                    f'Hi {funder} : New update for funded project {instance.project} - {instance.header}',
                    instance.body,
                    settings.DEFAULT_FROM_EMAIL,
                    [{funder}],
                    fail_silently=False,
                )
