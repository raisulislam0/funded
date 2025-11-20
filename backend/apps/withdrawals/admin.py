"""
Admin configuration for withdrawals app.
"""
from django.contrib import admin
from .models import Withdrawal


@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    """Admin for withdrawals."""
    
    list_display = ['campaign', 'creator', 'amount', 'payment_method', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['campaign__title', 'creator__email', 'account_number']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Campaign & Creator', {
            'fields': ('campaign', 'creator')
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

