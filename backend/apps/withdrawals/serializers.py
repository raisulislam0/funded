"""
Serializers for withdrawals app.
"""
from rest_framework import serializers
from .models import Withdrawal
from apps.campaigns.models import Campaign


class WithdrawalSerializer(serializers.ModelSerializer):
    """Serializer for withdrawals."""

    campaign_title = serializers.CharField(source='campaign.title', read_only=True)
    creator_name = serializers.CharField(source='creator.full_name', read_only=True)
    available_balance = serializers.SerializerMethodField()

    class Meta:
        model = Withdrawal
        fields = [
            'id', 'campaign_title', 'creator_name', 'amount', 'currency',
            'payment_method', 'account_number', 'account_name',
            'bank_name', 'branch_name', 'status', 'reviewed_at',
            'rejection_reason', 'processed_at', 'transaction_reference',
            'available_balance', 'created_at'
        ]
        read_only_fields = ['id', 'status', 'reviewed_at', 'rejection_reason', 'processed_at', 'transaction_reference', 'created_at']

    def get_available_balance(self, obj):
        """Get available balance for the campaign."""
        if obj.campaign:
            return float(obj.campaign.net_amount - obj.campaign.withdrawn_amount)
        return 0


class CreateWithdrawalSerializer(serializers.ModelSerializer):
    """Serializer for creating withdrawal requests."""

    class Meta:
        model = Withdrawal
        fields = [
            'campaign', 'amount', 'payment_method', 'account_number',
            'account_name', 'bank_name', 'branch_name', 'notes'
        ]

    def validate_campaign(self, value):
        """Validate that the user is the campaign creator."""
        request = self.context.get('request')
        if request and value.creator != request.user:
            raise serializers.ValidationError(
                "You can only request withdrawals for your own campaigns."
            )
        return value

    def validate_amount(self, value):
        """Validate withdrawal amount is positive."""
        if value <= 0:
            raise serializers.ValidationError(
                "Withdrawal amount must be greater than 0."
            )
        return value

    def validate(self, data):
        """Validate withdrawal request."""
        campaign = data.get('campaign')
        amount = data.get('amount')

        if campaign and amount:
            # Check if withdrawal amount is valid
            can_withdraw, error_msg = campaign.can_withdraw(amount)
            if not can_withdraw:
                raise serializers.ValidationError({
                    'amount': error_msg
                })

        return data

