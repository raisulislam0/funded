"""
Badge and gamification models.
"""
from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import TimeStampedModel

User = get_user_model()


class Badge(TimeStampedModel):
    """Badge definition."""
    
    BADGE_TYPE_CHOICES = [
        ('donor', 'Donor Badge'),
        ('creator', 'Creator Badge'),
        ('milestone', 'Milestone Badge'),
    ]
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    badge_type = models.CharField(max_length=20, choices=BADGE_TYPE_CHOICES)
    icon_url = models.URLField(blank=True, null=True)
    
    # Criteria
    criteria_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    criteria_count = models.IntegerField(null=True, blank=True)
    
    # Display
    color = models.CharField(max_length=7, default='#000000')
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'badges'
        verbose_name = 'Badge'
        verbose_name_plural = 'Badges'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class UserBadge(TimeStampedModel):
    """User earned badges."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='user_badges')
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_badges'
        verbose_name = 'User Badge'
        verbose_name_plural = 'User Badges'
        unique_together = ['user', 'badge']
        ordering = ['-earned_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.badge.name}"

