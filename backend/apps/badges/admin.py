"""
Admin configuration for badges app.
"""
from django.contrib import admin
from .models import Badge, UserBadge


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    """Admin for badges."""
    
    list_display = ['name', 'badge_type', 'is_active', 'created_at']
    list_filter = ['badge_type', 'is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    """Admin for user badges."""
    
    list_display = ['user', 'badge', 'earned_at']
    list_filter = ['badge', 'earned_at']
    search_fields = ['user__email', 'badge__name']

