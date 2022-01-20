from django.db import models
from django.conf import settings

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    class  Meta:
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.name
    def get_friendly_name(self):
        return self.friendly_name

class Project(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)

    name = models.CharField(max_length=254)
    description = models.TextField()
    
    price = models.DecimalField(max_digits=6, decimal_places=2)

    startDate = models.DateField()
    endDate = models.DateField(null=True, blank=True)

    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.name

class Comment(models.Model):
    item = models.ForeignKey('Project', null=True, blank=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'Comment "{self.body}" by {self.owner}'