"""
Management command to recalculate campaign withdrawn amounts from completed withdrawals.
"""
from django.core.management.base import BaseCommand
from django.db.models import Sum
from apps.campaigns.models import Campaign
from apps.withdrawals.models import Withdrawal


class Command(BaseCommand):
    help = 'Recalculate campaign withdrawn_amount from completed withdrawals'

    def handle(self, *args, **options):
        campaigns = Campaign.objects.all()
        updated_count = 0
        
        self.stdout.write('Starting withdrawal recalculation...')
        
        for campaign in campaigns:
            # Get all completed withdrawals for this campaign
            completed_withdrawals = Withdrawal.objects.filter(
                campaign=campaign,
                status='completed'
            )
            
            # Calculate total withdrawn amount
            total_withdrawn = completed_withdrawals.aggregate(
                total=Sum('amount')
            )['total'] or 0
            
            # Update campaign
            old_withdrawn = campaign.withdrawn_amount
            campaign.withdrawn_amount = total_withdrawn
            campaign.save(update_fields=['withdrawn_amount'])
            
            updated_count += 1
            
            if total_withdrawn > 0:
                self.stdout.write(
                    f'  Campaign: {campaign.title} - '
                    f'Withdrawn: {old_withdrawn} -> {total_withdrawn} BDT'
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated_count} campaigns')
        )

