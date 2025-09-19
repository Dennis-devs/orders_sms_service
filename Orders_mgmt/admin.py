from django.contrib import admin

# Register your models here.
from .models import Customer, Order

class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('time',)

admin.site.register(Customer)
admin.site.register(Order, OrderAdmin)