"""
Admin configuration for campaigns app.
"""
from django.contrib import admin
from .models import Category, Campaign, CampaignDocument, CampaignImage, CampaignUpdate, CampaignComment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin for campaign categories."""
    
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class CampaignDocumentInline(admin.TabularInline):
    """Inline admin for campaign documents."""
    model = CampaignDocument
    extra = 0


class CampaignImageInline(admin.TabularInline):
    """Inline admin for campaign images."""
    model = CampaignImage
    extra = 0


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    """Admin for campaigns."""

    list_display = ['title', 'creator', 'category', 'status', 'goal_amount', 'current_amount', 'withdrawn_amount', 'available_balance', 'progress_percentage', 'created_at']
    list_filter = ['status', 'category', 'is_featured', 'created_at']
    search_fields = ['title', 'creator__email', 'description']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['current_amount', 'withdrawn_amount', 'net_amount', 'available_balance', 'total_donors', 'total_donations', 'created_at', 'updated_at']
    inlines = [CampaignDocumentInline, CampaignImageInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('creator', 'title', 'slug', 'category')
        }),
        ('Description', {
            'fields': ('short_description', 'description')
        }),
        ('Media', {
            'fields': ('cover_image', 'video_url')
        }),
        ('Funding', {
            'fields': ('goal_amount', 'current_amount', 'net_amount', 'withdrawn_amount', 'available_balance', 'currency')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date')
        }),
        ('Status', {
            'fields': ('status', 'is_featured')
        }),
        ('Review', {
            'fields': ('reviewed_by', 'reviewed_at', 'rejection_reason')
        }),
        ('Statistics', {
            'fields': ('total_donors', 'total_donations')
        }),
        ('Location', {
            'fields': ('location', 'district')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(CampaignUpdate)
class CampaignUpdateAdmin(admin.ModelAdmin):
    """Admin for campaign updates."""
    
    list_display = ['campaign', 'title', 'created_at']
    list_filter = ['created_at']
    search_fields = ['campaign__title', 'title', 'content']


@admin.register(CampaignComment)
class CampaignCommentAdmin(admin.ModelAdmin):
    """Admin for campaign comments."""
    
    list_display = ['campaign', 'user', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['campaign__title', 'user__email', 'content']

