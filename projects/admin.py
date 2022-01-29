from django.contrib import admin
from .models import Project, Category, Comment, Update
# Register your models here.


#class ProjectAdmin(admin.ModelAdmin):
#    list_display = (
#        'name',
#        'category'
#    )
#    ordering = ('sku',)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


admin.site.register(Project)#, ProjectAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
admin.site.register(Update)