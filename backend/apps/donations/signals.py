"""
Signals for donations app.
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum, Count, Q
from .models import Donation


@receiver(post_save, sender=Donation)
def update_campaign_on_donation_save(sender, instance, created, **kwargs):
    """
    Update campaign statistics when a donation is saved.
    Only count completed donations towards campaign totals.
    """
    campaign = instance.campaign
    
    # Get all completed donations for this campaign
    completed_donations = Donation.objects.filter(
        campaign=campaign,
        status='completed'
    )
    
    # Calculate total amount from completed donations
    total_amount = completed_donations.aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    # Count total completed donations
    total_donations_count = completed_donations.count()
    
    # Count unique donors (both authenticated and anonymous)
    # For authenticated users, count unique donor IDs
    # For anonymous, count each donation as a separate donor
    authenticated_donors = completed_donations.filter(
        donor__isnull=False
    ).values('donor').distinct().count()
    
    anonymous_donors = completed_donations.filter(
        donor__isnull=True
    ).count()
    
    total_donors_count = authenticated_donors + anonymous_donors
    
    # Update campaign
    campaign.current_amount = total_amount
    campaign.total_donations = total_donations_count
    campaign.total_donors = total_donors_count
    campaign.save(update_fields=['current_amount', 'total_donations', 'total_donors'])


@receiver(post_delete, sender=Donation)
def update_campaign_on_donation_delete(sender, instance, **kwargs):
    """
    Update campaign statistics when a donation is deleted.
    """
    campaign = instance.campaign
    
    # Get all completed donations for this campaign
    completed_donations = Donation.objects.filter(
        campaign=campaign,
        status='completed'
    )
    
    # Calculate total amount from completed donations
    total_amount = completed_donations.aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    # Count total completed donations
    total_donations_count = completed_donations.count()
    
    # Count unique donors
    authenticated_donors = completed_donations.filter(
        donor__isnull=False
    ).values('donor').distinct().count()
    
    anonymous_donors = completed_donations.filter(
        donor__isnull=True
    ).count()
    
    total_donors_count = authenticated_donors + anonymous_donors
    
    # Update campaign
    campaign.current_amount = total_amount
    campaign.total_donations = total_donations_count
    campaign.total_donors = total_donors_count
    campaign.save(update_fields=['current_amount', 'total_donations', 'total_donors'])

