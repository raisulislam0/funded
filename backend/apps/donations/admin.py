"""
Admin configuration for donations app.
"""
from django.contrib import admin
from .models import Donation, Transaction, PaymentWebhook


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    """Admin for donations."""

    list_display = ['transaction_id', 'donor', 'campaign', 'amount', 'status', 'payment_method', 'created_at']
    list_filter = ['status', 'payment_method', 'is_anonymous', 'created_at']
    search_fields = ['transaction_id', 'donor__email', 'campaign__title', 'donor_email']
    readonly_fields = ['transaction_id', 'platform_fee', 'net_amount', 'created_at', 'updated_at']

    fieldsets = (
        ('Campaign', {
            'fields': ('campaign',)
        }),
        ('Donor Information', {
            'fields': ('donor', 'is_anonymous', 'donor_name', 'donor_email')
        }),
        ('Payment Details', {
            'fields': ('amount', 'platform_fee', 'net_amount', 'currency', 'payment_method', 'payment_reference')
        }),
        ('Transaction', {
            'fields': ('transaction_id', 'status')
        }),
        ('Optional', {
            'fields': ('message',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """Auto-calculate platform fee before saving."""
        if obj.amount and not obj.platform_fee:
            from apps.core.utils import calculate_platform_fee
            obj.platform_fee = calculate_platform_fee(obj.amount)
        super().save_model(request, obj, form, change)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Admin for transactions."""
    
    list_display = ['transaction_id', 'transaction_type', 'amount', 'payment_gateway', 'status', 'created_at']
    list_filter = ['transaction_type', 'payment_gateway', 'status', 'created_at']
    search_fields = ['transaction_id', 'gateway_transaction_id']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(PaymentWebhook)
class PaymentWebhookAdmin(admin.ModelAdmin):
    """Admin for payment webhooks."""
    
    list_display = ['gateway', 'event_type', 'is_processed', 'created_at']
    list_filter = ['gateway', 'is_processed', 'created_at']
    readonly_fields = ['created_at', 'updated_at']

