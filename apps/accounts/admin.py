from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, ClientProfile

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'phone', 'user_type', 'status', 'kyc_status', 'date_joined']
    list_filter = ['user_type', 'status', 'kyc_status']
    search_fields = ['email', 'phone', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('phone', 'phone_verified', 'user_type', 'status', 
                      'kyc_status', 'language_preference', 'profile_picture_url')
        }),
    )

@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_trips', 'total_spent', 'average_rating']
    search_fields = ['user__email', 'user__phone']

