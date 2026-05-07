from django.contrib import admin
from .models import Customer

class CustomerAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Customer model.
    """
    list_display = ('code', 'name', 'email', 'city', 'country')

admin.site.register(Customer, CustomerAdmin)