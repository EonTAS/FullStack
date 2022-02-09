from django.contrib import admin
from .models import Commission


class CommissionAdmin(admin.ModelAdmin):
    readonly_fields = ('order_number', 'date', 'order_price')
    ordering = ('-date',)  # reverse order by date


admin.site.register(Commission, CommissionAdmin)
