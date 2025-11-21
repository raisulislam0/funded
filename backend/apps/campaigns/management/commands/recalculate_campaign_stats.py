"""
Management command to recalculate campaign statistics from donations.
"""
from django.core.management.base import BaseCommand
from django.db.models import Sum, Count
from apps.campaigns.models import Campaign
from apps.donations.models import Donation


class Command(BaseCommand):
    help = 'Recalculate campaign statistics (current_amount, total_donors, total_donations) from completed donations'

    def handle(self, *args, **options):
        campaigns = Campaign.objects.all()
        updated_count = 0
        
        self.stdout.write('Starting campaign statistics recalculation...')
        
        for campaign in campaigns:
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
            old_amount = campaign.current_amount
            campaign.current_amount = total_amount
            campaign.total_donations = total_donations_count
            campaign.total_donors = total_donors_count
            campaign.save(update_fields=['current_amount', 'total_donations', 'total_donors'])
            
            updated_count += 1
            
            self.stdout.write(
                f'  Campaign: {campaign.title} - '
                f'Amount: {old_amount} -> {total_amount}, '
                f'Donations: {total_donations_count}, '
                f'Donors: {total_donors_count}'
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated_count} campaigns')
        )

