from django.contrib import admin
from .models import Project, Category, Comment, Update
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


admin.site.register(Project)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
admin.site.register(Update)
