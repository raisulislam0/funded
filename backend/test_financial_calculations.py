"""
Quick script to test financial calculations.
Run with: python manage.py shell < test_financial_calculations.py
"""
from decimal import Decimal
from apps.campaigns.models import Campaign
from apps.donations.models import Donation
from apps.withdrawals.models import Withdrawal

print("\n" + "="*80)
print("FINANCIAL CALCULATION TEST")
print("="*80)

# Get all campaigns
campaigns = Campaign.objects.all()

for campaign in campaigns:
    print(f"\n📊 Campaign: {campaign.title}")
    print(f"   Creator: {campaign.creator.email}")
    print("-" * 80)
    
    # Get donations
    all_donations = campaign.donations.all()
    completed_donations = campaign.donations.filter(status='completed')
    
    print(f"\n💰 DONATIONS:")
    print(f"   Total donations (all): {all_donations.count()}")
    print(f"   Completed donations: {completed_donations.count()}")
    
    if completed_donations.exists():
        for donation in completed_donations:
            print(f"   - {donation.amount} BDT (fee: {donation.platform_fee}, net: {donation.net_amount}) - {donation.status}")
    
    # Calculate totals
    total_amount = sum(d.amount for d in completed_donations)
    total_fees = sum(d.platform_fee for d in completed_donations)
    total_net = sum(d.net_amount for d in completed_donations)
    
    print(f"\n   Calculated Totals:")
    print(f"   - Total Amount: {total_amount} BDT")
    print(f"   - Total Fees: {total_fees} BDT")
    print(f"   - Total Net: {total_net} BDT")
    
    print(f"\n   Campaign Fields:")
    print(f"   - current_amount: {campaign.current_amount} BDT")
    print(f"   - net_amount (property): {campaign.net_amount} BDT")
    print(f"   - withdrawn_amount: {campaign.withdrawn_amount} BDT")
    print(f"   - available_balance (property): {campaign.available_balance} BDT")
    
    # Get withdrawals
    all_withdrawals = campaign.withdrawals.all()
    completed_withdrawals = campaign.withdrawals.filter(status='completed')
    
    print(f"\n💸 WITHDRAWALS:")
    print(f"   Total withdrawals (all): {all_withdrawals.count()}")
    print(f"   Completed withdrawals: {completed_withdrawals.count()}")
    
    if all_withdrawals.exists():
        for withdrawal in all_withdrawals:
            print(f"   - {withdrawal.amount} BDT - {withdrawal.status}")
    
    # Validation
    print(f"\n✅ VALIDATION:")
    can_withdraw_1000, msg = campaign.can_withdraw(Decimal('1000'))
    print(f"   Can withdraw 1000 BDT? {can_withdraw_1000}")
    if not can_withdraw_1000:
        print(f"   Error: {msg}")
    
    can_withdraw_all, msg = campaign.can_withdraw(campaign.available_balance)
    print(f"   Can withdraw all available ({campaign.available_balance} BDT)? {can_withdraw_all}")
    if not can_withdraw_all:
        print(f"   Error: {msg}")
    
    print("\n" + "="*80)

print("\n✅ Test complete!\n")

