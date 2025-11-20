"""
Serializers for withdrawals app.
"""
from rest_framework import serializers
from .models import Withdrawal


class WithdrawalSerializer(serializers.ModelSerializer):
    """Serializer for withdrawals."""
    
    campaign_title = serializers.CharField(source='campaign.title', read_only=True)
    creator_name = serializers.CharField(source='creator.full_name', read_only=True)
    
    class Meta:
        model = Withdrawal
        fields = [
            'id', 'campaign_title', 'creator_name', 'amount', 'currency',
            'payment_method', 'account_number', 'account_name',
            'bank_name', 'branch_name', 'status', 'reviewed_at',
            'rejection_reason', 'processed_at', 'transaction_reference',
            'created_at'
        ]
        read_only_fields = ['id', 'status', 'reviewed_at', 'rejection_reason', 'processed_at', 'transaction_reference', 'created_at']


class CreateWithdrawalSerializer(serializers.ModelSerializer):
    """Serializer for creating withdrawal requests."""
    
    class Meta:
        model = Withdrawal
        fields = [
            'campaign', 'amount', 'payment_method', 'account_number',
            'account_name', 'bank_name', 'branch_name', 'notes'
        ]

