"""
Serializers for donations app.
"""
from rest_framework import serializers
from .models import Donation, Transaction


class DonationSerializer(serializers.ModelSerializer):
    """Serializer for donations."""
    
    donor_name_display = serializers.SerializerMethodField()
    campaign_title = serializers.CharField(source='campaign.title', read_only=True)
    
    class Meta:
        model = Donation
        fields = [
            'id', 'donor_name_display', 'campaign_title', 'amount',
            'platform_fee', 'net_amount', 'currency', 'transaction_id',
            'payment_method', 'status', 'message', 'created_at'
        ]
        read_only_fields = ['id', 'transaction_id', 'platform_fee', 'net_amount', 'status', 'created_at']
    
    def get_donor_name_display(self, obj):
        if obj.is_anonymous:
            return 'Anonymous'
        return obj.donor.full_name if obj.donor else obj.donor_name


class CreateDonationSerializer(serializers.Serializer):
    """Serializer for creating a donation."""
    
    campaign_id = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=10)
    payment_method = serializers.ChoiceField(choices=['bkash', 'nagad'])
    is_anonymous = serializers.BooleanField(default=False)
    message = serializers.CharField(required=False, allow_blank=True)
    donor_name = serializers.CharField(required=False, allow_blank=True)
    donor_email = serializers.EmailField(required=False, allow_blank=True)


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for transactions."""
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'transaction_id', 'transaction_type', 'amount',
            'currency', 'payment_gateway', 'status', 'created_at'
        ]

