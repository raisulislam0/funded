"""
Withdrawal models.
"""
from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import TimeStampedModel
from apps.campaigns.models import Campaign

User = get_user_model()


class Withdrawal(TimeStampedModel):
    """Withdrawal request model."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('bkash', 'bKash'),
        ('nagad', 'Nagad'),
        ('bank', 'Bank Transfer'),
    ]
    
    # Campaign and creator
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='withdrawals')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='withdrawals')
    
    # Amount
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='BDT')
    
    # Payment details
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    account_number = models.CharField(max_length=100)
    account_name = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    branch_name = models.CharField(max_length=255, blank=True, null=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Review
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_withdrawals'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True, null=True)
    
    # Processing
    processed_at = models.DateTimeField(null=True, blank=True)
    transaction_reference = models.CharField(max_length=255, blank=True, null=True)
    
    # Notes
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'withdrawals'
        verbose_name = 'Withdrawal'
        verbose_name_plural = 'Withdrawals'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['campaign', 'status']),
            models.Index(fields=['creator', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.creator.email} - {self.amount} BDT - {self.status}"

