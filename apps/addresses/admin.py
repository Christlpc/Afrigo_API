from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from .models import Address

@admin.register(Address)
class AddressAdmin(GISModelAdmin):
    list_display = ['full_address', 'user', 'city', 'is_favorite', 'created_at']
    list_filter = ['is_favorite', 'city', 'created_at']
    search_fields = ['full_address', 'user__email']
    readonly_fields = ['created_at', 'updated_at']

