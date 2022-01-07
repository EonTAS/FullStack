from django.contrib import admin
from .models import Project, Category
# Register your models here.


class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category'
    )
    ordering = ('sku',)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


admin.site.register(Project, ProjectAdmin)
admin.site.register(Category, CategoryAdmin)