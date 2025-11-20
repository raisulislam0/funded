"""
Donation and transaction models.
"""
from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import TimeStampedModel
from apps.campaigns.models import Campaign

User = get_user_model()


class Donation(TimeStampedModel):
    """Donation model."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    # Donor information
    donor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='donations'
    )
    is_anonymous = models.BooleanField(default=False)
    donor_name = models.CharField(max_length=255, blank=True, null=True)
    donor_email = models.EmailField(blank=True, null=True)
    
    # Campaign
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='donations')
    
    # Amount
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    platform_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='BDT')
    
    # Transaction
    transaction_id = models.CharField(max_length=100, unique=True)
    payment_method = models.CharField(max_length=50)  # bkash, nagad, etc.
    payment_reference = models.CharField(max_length=255, blank=True, null=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Optional message
    message = models.TextField(blank=True, null=True)
    
    # Metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'donations'
        verbose_name = 'Donation'
        verbose_name_plural = 'Donations'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['campaign', 'status']),
            models.Index(fields=['donor', '-created_at']),
            models.Index(fields=['transaction_id']),
        ]
    
    def __str__(self):
        donor_display = self.donor.email if self.donor else 'Anonymous'
        return f"{donor_display} - {self.amount} BDT to {self.campaign.title}"
    
    def save(self, *args, **kwargs):
        # Calculate net amount
        if not self.net_amount:
            self.net_amount = self.amount - self.platform_fee
        super().save(*args, **kwargs)


class Transaction(TimeStampedModel):
    """Payment transaction log."""
    
    TRANSACTION_TYPE_CHOICES = [
        ('donation', 'Donation'),
        ('refund', 'Refund'),
        ('withdrawal', 'Withdrawal'),
    ]
    
    STATUS_CHOICES = [
        ('initiated', 'Initiated'),
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Transaction details
    transaction_id = models.CharField(max_length=100, unique=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    
    # Related objects
    donation = models.ForeignKey(
        Donation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions'
    )
    
    # Amount
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='BDT')
    
    # Payment gateway
    payment_gateway = models.CharField(max_length=50)  # bkash, nagad
    gateway_transaction_id = models.CharField(max_length=255, blank=True, null=True)
    gateway_response = models.JSONField(default=dict, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='initiated')
    
    # Error handling
    error_message = models.TextField(blank=True, null=True)
    retry_count = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'transactions'
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['transaction_id']),
            models.Index(fields=['gateway_transaction_id']),
            models.Index(fields=['status', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.transaction_id} - {self.transaction_type} - {self.status}"


class PaymentWebhook(TimeStampedModel):
    """Log of payment gateway webhooks."""
    
    gateway = models.CharField(max_length=50)
    event_type = models.CharField(max_length=100)
    payload = models.JSONField()
    headers = models.JSONField(default=dict)
    
    # Processing
    is_processed = models.BooleanField(default=False)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    # Related transaction
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='webhooks'
    )
    
    class Meta:
        db_table = 'payment_webhooks'
        verbose_name = 'Payment Webhook'
        verbose_name_plural = 'Payment Webhooks'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.gateway} - {self.event_type} - {self.created_at}"

