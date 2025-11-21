"""
Tests for withdrawal financial logic.
"""
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from apps.campaigns.models import Campaign, Category
from apps.donations.models import Donation
from apps.withdrawals.models import Withdrawal
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class WithdrawalFinancialTests(TestCase):
    """Test financial transaction logic for withdrawals."""
    
    def setUp(self):
        """Set up test data."""
        # Create users
        self.creator = User.objects.create_user(
            email='creator@test.com',
            password='testpass123',
            full_name='Test Creator',
            user_type='creator'
        )
        
        self.donor = User.objects.create_user(
            email='donor@test.com',
            password='testpass123',
            full_name='Test Donor',
            user_type='donor'
        )
        
        # Create category
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        
        # Create campaign
        self.campaign = Campaign.objects.create(
            creator=self.creator,
            title='Test Campaign',
            slug='test-campaign',
            category=self.category,
            short_description='Test description',
            description='Test long description',
            cover_image='https://example.com/image.jpg',
            goal_amount=Decimal('10000.00'),
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=30),
            status='active'
        )
    
    def test_withdrawal_validation_insufficient_balance(self):
        """Test that withdrawal fails when balance is insufficient."""
        # Try to withdraw without any donations
        withdrawal = Withdrawal(
            campaign=self.campaign,
            creator=self.creator,
            amount=Decimal('1000.00'),
            payment_method='bkash',
            account_number='01700000000',
            account_name='Test Creator'
        )
        
        # Should raise validation error
        with self.assertRaises(ValidationError):
            withdrawal.full_clean()
    
    def test_withdrawal_validation_with_sufficient_balance(self):
        """Test that withdrawal succeeds with sufficient balance."""
        # Create a completed donation
        donation = Donation.objects.create(
            campaign=self.campaign,
            donor=self.donor,
            amount=Decimal('5000.00'),
            platform_fee=Decimal('250.00'),  # 5% fee
            net_amount=Decimal('4750.00'),
            transaction_id='TEST-DON-001',
            payment_method='bkash',
            status='completed'
        )

        # Refresh campaign to get updated amounts
        self.campaign.refresh_from_db()

        # Verify campaign amounts are correct
        self.assertEqual(self.campaign.current_amount, Decimal('5000.00'))
        self.assertEqual(self.campaign.net_amount, Decimal('4750.00'))
        self.assertEqual(self.campaign.available_balance, Decimal('4750.00'))

        # Try to withdraw less than net amount
        withdrawal = Withdrawal(
            campaign=self.campaign,
            creator=self.creator,
            amount=Decimal('4000.00'),
            payment_method='bkash',
            account_number='01700000000',
            account_name='Test Creator'
        )

        # Should not raise validation error
        withdrawal.full_clean()
        withdrawal.save()

        self.assertEqual(withdrawal.status, 'pending')

    def test_withdrawal_cannot_exceed_net_amount(self):
        """Test that withdrawal cannot exceed net amount (after platform fees)."""
        # Create a donation of 2000 BDT with 5% fee
        donation = Donation.objects.create(
            campaign=self.campaign,
            donor=self.donor,
            amount=Decimal('2000.00'),
            platform_fee=Decimal('100.00'),  # 5% fee
            net_amount=Decimal('1900.00'),
            transaction_id='TEST-DON-003',
            payment_method='bkash',
            status='completed'
        )

        # Refresh campaign
        self.campaign.refresh_from_db()

        # Verify amounts
        self.assertEqual(self.campaign.current_amount, Decimal('2000.00'))
        self.assertEqual(self.campaign.net_amount, Decimal('1900.00'))
        self.assertEqual(self.campaign.available_balance, Decimal('1900.00'))

        # Try to withdraw 2000 BDT (more than net amount)
        withdrawal = Withdrawal(
            campaign=self.campaign,
            creator=self.creator,
            amount=Decimal('2000.00'),
            payment_method='bkash',
            account_number='01700000000',
            account_name='Test Creator'
        )

        # Should raise validation error
        with self.assertRaises(ValidationError) as context:
            withdrawal.full_clean()

        # Check error message mentions available balance
        self.assertIn('1900', str(context.exception))

    def test_available_balance_uses_net_amount(self):
        """Test that available_balance is calculated from net_amount, not current_amount."""
        # Create donation
        donation = Donation.objects.create(
            campaign=self.campaign,
            donor=self.donor,
            amount=Decimal('1000.00'),
            platform_fee=Decimal('50.00'),
            net_amount=Decimal('950.00'),
            transaction_id='TEST-DON-004',
            payment_method='bkash',
            status='completed'
        )

        # Refresh campaign
        self.campaign.refresh_from_db()

        # available_balance should be net_amount (950), not current_amount (1000)
        self.assertEqual(self.campaign.available_balance, Decimal('950.00'))
        self.assertNotEqual(self.campaign.available_balance, Decimal('1000.00'))
    
    def test_withdrawal_updates_campaign_withdrawn_amount(self):
        """Test that completing withdrawal updates campaign withdrawn_amount."""
        # Create donation
        donation = Donation.objects.create(
            campaign=self.campaign,
            donor=self.donor,
            amount=Decimal('5000.00'),
            platform_fee=Decimal('250.00'),
            net_amount=Decimal('4750.00'),
            transaction_id='TEST-DON-002',
            payment_method='bkash',
            status='completed'
        )
        
        # Create and complete withdrawal
        withdrawal = Withdrawal.objects.create(
            campaign=self.campaign,
            creator=self.creator,
            amount=Decimal('2000.00'),
            payment_method='bkash',
            account_number='01700000000',
            account_name='Test Creator',
            status='pending'
        )
        
        # Complete the withdrawal
        withdrawal.status = 'completed'
        withdrawal.save()
        
        # Refresh campaign
        self.campaign.refresh_from_db()
        
        # Check withdrawn_amount is updated
        self.assertEqual(self.campaign.withdrawn_amount, Decimal('2000.00'))
        
        # Check available balance
        expected_available = Decimal('4750.00') - Decimal('2000.00')
        self.assertEqual(self.campaign.available_balance, expected_available)

