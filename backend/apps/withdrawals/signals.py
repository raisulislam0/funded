"""
Signals for withdrawals app.
ACID-compliant financial transaction handling.
"""
from django.db import transaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from decimal import Decimal
from .models import Withdrawal


@receiver(pre_save, sender=Withdrawal)
def validate_withdrawal_before_save(sender, instance, **kwargs):
    """
    Validate withdrawal before saving.
    This runs before the save to catch issues early.
    """
    # Only validate on status changes to 'completed'
    if instance.pk:
        try:
            old_instance = Withdrawal.objects.get(pk=instance.pk)
            # If status is changing to completed, validate
            if old_instance.status != 'completed' and instance.status == 'completed':
                # Calculate what the total would be if this withdrawal completes
                campaign = instance.campaign

                # Get all OTHER completed withdrawals
                other_completed = Withdrawal.objects.filter(
                    campaign=campaign,
                    status='completed'
                ).exclude(pk=instance.pk)

                other_total = other_completed.aggregate(
                    total=models.Sum('amount')
                )['total'] or Decimal('0')

                # Add this withdrawal amount
                new_total = other_total + instance.amount

                # Check against net amount
                net_amount = campaign.net_amount
                if new_total > net_amount:
                    raise ValidationError(
                        f"Cannot complete withdrawal: Total withdrawals would be {new_total} BDT, "
                        f"but only {net_amount} BDT is available (after platform fees). "
                        f"Already withdrawn: {other_total} BDT."
                    )
        except Withdrawal.DoesNotExist:
            pass


@receiver(post_save, sender=Withdrawal)
def update_campaign_on_withdrawal(sender, instance, created, **kwargs):
    """
    Update campaign withdrawn_amount when withdrawal is completed.
    Uses database transaction to ensure ACID compliance.

    Only completed withdrawals affect the campaign's withdrawn_amount.
    This signal ONLY updates the withdrawn_amount field and does NOT validate.
    Validation happens in:
    1. Withdrawal.clean() - for initial creation
    2. pre_save signal - when status changes to 'completed'
    """
    # Use atomic transaction to ensure data consistency
    with transaction.atomic():
        # Lock the campaign row for update to prevent race conditions
        campaign = instance.campaign.__class__.objects.select_for_update().get(pk=instance.campaign.pk)

        # Calculate total completed withdrawals for this campaign
        completed_withdrawals = Withdrawal.objects.filter(
            campaign=campaign,
            status='completed'
        )

        total_withdrawn = completed_withdrawals.aggregate(
            total=models.Sum('amount')
        )['total'] or Decimal('0')

        # Update campaign withdrawn_amount
        # No validation here - validation happens before save
        campaign.withdrawn_amount = total_withdrawn
        campaign.save(update_fields=['withdrawn_amount'])


# Import models at the end to avoid circular imports
from django.db import models

