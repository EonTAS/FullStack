from django.db import models
from django.conf import settings


from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.mail import send_mail

from django.core.exceptions import ObjectDoesNotExist

# each project can be any of these categories


class Category(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    examplePrice_shortterm = models.DecimalField(max_digits=6, decimal_places=2)
    examplePrice_midterm = models.DecimalField(max_digits=6, decimal_places=2)
    examplePrice_longterm = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.friendly_name

# each project in the site


class Project(models.Model):
    category = models.ForeignKey('Category', on_delete=models.PROTECT)

    name = models.CharField(max_length=254)
    description = models.TextField()

    # price listing for the project
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

# superclass to Comments and Updates, a notification for a project


class Message(models.Model):
    item = models.ForeignKey('Project', null=True,
                             blank=True, on_delete=models.SET_NULL)
    header = models.CharField(max_length=255)
    body = models.TextField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']
        abstract = True


class Comment(Message):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'Comment "{self.body}" by {self.owner}'


class Update(Message):  # associated with account, account views all they have funded + able to see updates specifically for those ones in a special view
    def __str__(self):
        return f'{self.item} update {self.created_on}'

    # function to send the email to the user if they have it enabled
    def sendEmail(self):
        suggester = self.item.suggester
        # if the item doesnt have a related commission, funder doesnt exist so set to None
        try:
            funder = self.item.commission.user
        except Exception as e:
            funder = None
        body = self.body + \
            "\n\nIf you have any issue, please respond to this email and we will get back to you (not really this is a fake email)"
        if suggester == funder:  # if suggester and funder are the same person, dont send two emails, just the one that makes sense
            if suggester.userprofile.email_updates:
                send_mail(
                    f'Hi {suggester} : New update for suggested and funded project {self.item} - {self.header}',
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [{suggester.email}],
                    fail_silently=False,
                )
        else:  # else check each setting individually and send seperate emails
            if suggester.userprofile.email_updates:
                send_mail(
                    f'Hi {suggester} : New update for suggested idea {self.item} - {self.header}',
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [{suggester.email}],
                    fail_silently=False,
                )
            if funder and funder.userprofile.email_updates:  # only send to funder if they exist
                send_mail(
                    f'Hi {funder} : New update for funded project {self.item} - {self.header}',
                    body,
                    self.DEFAULT_FROM_EMAIL,
                    [{funder.email}],
                    fail_silently=False,
                )


@receiver(post_save, sender=Update)
def sendUpdate(sender, instance, created, **kwargs):
    if created:
        instance.sendEmail()
