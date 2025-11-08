from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from .models import Route

@admin.register(Route)
class RouteAdmin(GISModelAdmin):
    list_display = ['id', 'client', 'driver', 'route_type', 'status', 'total_fare', 'payment_status', 'created_at']
    list_filter = ['route_type', 'status', 'payment_status', 'created_at']
    search_fields = ['client__email', 'driver__email']
    readonly_fields = ['created_at', 'updated_at']

