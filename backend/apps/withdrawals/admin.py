"""
Admin configuration for withdrawals app.
"""
from django.contrib import admin
from django.utils.html import format_html
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Withdrawal


@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    """Admin for withdrawals."""

    list_display = ['campaign', 'creator', 'amount', 'available_balance_display', 'payment_method', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['campaign__title', 'creator__email', 'account_number']
    readonly_fields = ['created_at', 'updated_at', 'campaign_balance_info']

    fieldsets = (
        ('Campaign & Creator', {
            'fields': ('campaign', 'creator', 'campaign_balance_info')
        }),
        ('Amount', {
            'fields': ('amount', 'currency')
        }),
        ('Payment Details', {
            'fields': ('payment_method', 'account_number', 'account_name', 'bank_name', 'branch_name')
        }),
        ('Status', {
            'fields': ('status', 'reviewed_by', 'reviewed_at', 'rejection_reason')
        }),
        ('Processing', {
            'fields': ('processed_at', 'transaction_reference', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def available_balance_display(self, obj):
        """Display available balance for the campaign."""
        if obj.campaign:
            net_amount = obj.campaign.net_amount
            withdrawn = obj.campaign.withdrawn_amount
            available = net_amount - withdrawn

            if available < obj.amount and obj.status == 'pending':
                return format_html(
                    '<span style="color: red; font-weight: bold;">{} BDT (Insufficient!)</span>',
                    available
                )
            return format_html('{} BDT', available)
        return '-'
    available_balance_display.short_description = 'Available Balance'

    def campaign_balance_info(self, obj):
        """Display detailed balance information for the campaign."""
        if obj.campaign:
            campaign = obj.campaign
            total_donations = campaign.current_amount
            net_amount = campaign.net_amount
            withdrawn = campaign.withdrawn_amount
            available = net_amount - withdrawn

            return format_html(
                '<div style="background: #f8f9fa; padding: 10px; border-radius: 5px;">'
                '<strong>Financial Summary:</strong><br>'
                'Total Donations: <strong>{}</strong> BDT<br>'
                'Net Amount (after fees): <strong>{}</strong> BDT<br>'
                'Already Withdrawn: <strong>{}</strong> BDT<br>'
                'Available Balance: <strong style="color: {};">{}</strong> BDT'
                '</div>',
                total_donations,
                net_amount,
                withdrawn,
                'green' if available >= obj.amount else 'red',
                available
            )
        return '-'
    campaign_balance_info.short_description = 'Campaign Balance'

    def save_model(self, request, obj, form, change):
        """Validate before saving."""
        try:
            # Set reviewed_by when status changes
            if change:
                old_obj = Withdrawal.objects.get(pk=obj.pk)
                if old_obj.status != obj.status and obj.status in ['approved', 'rejected', 'completed']:
                    obj.reviewed_by = request.user
                    from django.utils import timezone
                    obj.reviewed_at = timezone.now()

                    if obj.status == 'completed':
                        obj.processed_at = timezone.now()

            super().save_model(request, obj, form, change)

            # Show success message with balance info
            if obj.status == 'completed':
                remaining = obj.campaign.net_amount - obj.campaign.withdrawn_amount
                messages.success(
                    request,
                    f'Withdrawal completed. Remaining balance: {remaining} BDT'
                )
        except ValidationError as e:
            messages.error(request, str(e))
            raise

