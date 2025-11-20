"""
Admin configuration for accounts app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserVerification, UserProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin for custom user model."""
    
    list_display = ['email', 'full_name', 'user_type', 'is_verified', 'is_active', 'created_at']
    list_filter = ['user_type', 'is_verified', 'is_active', 'is_staff']
    search_fields = ['email', 'full_name', 'phone']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'phone', 'avatar', 'bio')}),
        ('User Type', {'fields': ('user_type',)}),
        ('Verification', {'fields': ('is_verified', 'is_email_verified', 'is_phone_verified', 'verified_at')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'last_login']


@admin.register(UserVerification)
class UserVerificationAdmin(admin.ModelAdmin):
    """Admin for user verification."""
    
    list_display = ['user', 'document_type', 'status', 'created_at', 'reviewed_at']
    list_filter = ['status', 'document_type']
    search_fields = ['user__email', 'document_number']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Document', {'fields': ('document_type', 'document_number', 'document_front_url', 'document_back_url', 'selfie_url')}),
        ('Address', {'fields': ('address_line', 'city', 'district', 'postal_code')}),
        ('Verification', {'fields': ('status', 'reviewed_by', 'reviewed_at', 'rejection_reason')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin for user profile."""
    
    list_display = ['user', 'total_donations', 'total_campaigns', 'total_raised']
    search_fields = ['user__email', 'user__full_name']
    readonly_fields = ['created_at', 'updated_at']

