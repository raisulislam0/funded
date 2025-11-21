"""
Campaign models.
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.core.models import TimeStampedModel

User = get_user_model()


class Category(TimeStampedModel):
    """Campaign categories."""
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Campaign(TimeStampedModel):
    """Main campaign model."""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Basic Information
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='campaigns')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='campaigns')
    
    # Description
    short_description = models.CharField(max_length=500)
    description = models.TextField()
    
    # Media
    cover_image = models.URLField()
    video_url = models.URLField(blank=True, null=True)
    
    # Funding
    goal_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    withdrawn_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='BDT')
    
    # Timeline
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    
    # Review
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_campaigns'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True, null=True)
    
    # Statistics (denormalized)
    total_donors = models.IntegerField(default=0)
    total_donations = models.IntegerField(default=0)
    
    # Location
    location = models.CharField(max_length=255, blank=True)
    district = models.CharField(max_length=100, blank=True)
    
    class Meta:
        db_table = 'campaigns'
        verbose_name = 'Campaign'
        verbose_name_plural = 'Campaigns'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['category', 'status']),
            models.Index(fields=['slug']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(withdrawn_amount__gte=0),
                name='withdrawn_amount_non_negative'
            ),
            models.CheckConstraint(
                check=models.Q(withdrawn_amount__lte=models.F('current_amount')),
                name='withdrawn_amount_lte_current_amount'
            ),
        ]
    
    def __str__(self):
        return self.title
    
    @property
    def progress_percentage(self):
        """Calculate funding progress percentage."""
        if self.goal_amount > 0:
            return min((self.current_amount / self.goal_amount) * 100, 100)
        return 0
    
    @property
    def is_active(self):
        """Check if campaign is currently active."""
        now = timezone.now()
        return (
            self.status == 'active' and
            self.start_date <= now <= self.end_date
        )
    
    @property
    def days_remaining(self):
        """Calculate days remaining until end date."""
        if self.end_date > timezone.now():
            delta = self.end_date - timezone.now()
            return delta.days
        return 0

    @property
    def available_balance(self):
        """
        Calculate available balance for withdrawal.
        This is the amount that can still be withdrawn.

        Important: This is calculated from net_amount (after platform fees),
        not current_amount (gross donations).
        """
        from decimal import Decimal
        return max(Decimal('0'), self.net_amount - self.withdrawn_amount)

    @property
    def net_amount(self):
        """
        Calculate net amount after platform fees.
        Platform fee is deducted from donations, so this shows
        the actual amount available to the campaign creator.
        """
        from apps.donations.models import Donation
        from decimal import Decimal

        # Sum up net_amount from all completed donations
        completed_donations = self.donations.filter(status='completed')
        total_net = completed_donations.aggregate(
            total=models.Sum('net_amount')
        )['total'] or Decimal('0')

        return total_net

    def can_withdraw(self, amount):
        """
        Check if a withdrawal amount is valid.

        Args:
            amount: Decimal amount to withdraw

        Returns:
            tuple: (bool, str) - (is_valid, error_message)
        """
        from decimal import Decimal

        if amount <= 0:
            return False, "Withdrawal amount must be greater than 0"

        # Check against net amount (after platform fees)
        net_available = self.net_amount - self.withdrawn_amount

        if amount > net_available:
            return False, f"Insufficient balance. Available: {net_available} BDT"

        return True, ""


class CampaignDocument(TimeStampedModel):
    """Supporting documents for campaigns."""
    
    DOCUMENT_TYPE_CHOICES = [
        ('medical', 'Medical Report'),
        ('financial', 'Financial Document'),
        ('legal', 'Legal Document'),
        ('other', 'Other'),
    ]
    
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    file_url = models.URLField()
    file_size = models.IntegerField(help_text='File size in bytes')
    
    class Meta:
        db_table = 'campaign_documents'
        verbose_name = 'Campaign Document'
        verbose_name_plural = 'Campaign Documents'
    
    def __str__(self):
        return f"{self.campaign.title} - {self.title}"


class CampaignImage(TimeStampedModel):
    """Additional images for campaigns."""
    
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField()
    caption = models.CharField(max_length=255, blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'campaign_images'
        verbose_name = 'Campaign Image'
        verbose_name_plural = 'Campaign Images'
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.campaign.title} - Image {self.order}"


class CampaignUpdate(TimeStampedModel):
    """Campaign updates posted by creators."""
    
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='updates')
    title = models.CharField(max_length=255)
    content = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    
    class Meta:
        db_table = 'campaign_updates'
        verbose_name = 'Campaign Update'
        verbose_name_plural = 'Campaign Updates'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.campaign.title} - {self.title}"


class CampaignComment(TimeStampedModel):
    """Comments on campaigns."""
    
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='campaign_comments')
    content = models.TextField()
    is_approved = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'campaign_comments'
        verbose_name = 'Campaign Comment'
        verbose_name_plural = 'Campaign Comments'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} on {self.campaign.title}"

