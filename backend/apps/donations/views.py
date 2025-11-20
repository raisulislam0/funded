"""
Views for donations app.
"""
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Donation, Transaction, PaymentWebhook
from .serializers import DonationSerializer, CreateDonationSerializer, TransactionSerializer
from apps.campaigns.models import Campaign
from apps.core.utils import generate_transaction_id, calculate_platform_fee


class DonationListView(generics.ListAPIView):
    """List donations (user's own donations if authenticated)."""
    
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Donation.objects.filter(donor=self.request.user)
        return Donation.objects.none()


class DonationDetailView(generics.RetrieveAPIView):
    """Get donation details."""
    
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Donation.objects.filter(donor=self.request.user)


class CreateDonationView(APIView):
    """Create a new donation and initiate payment."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = CreateDonationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        
        # Get campaign
        try:
            campaign = Campaign.objects.get(id=data['campaign_id'], status='active')
        except Campaign.DoesNotExist:
            return Response({
                'success': False,
                'error': {'message': 'Campaign not found or not active'}
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Calculate fees
        amount = data['amount']
        platform_fee = calculate_platform_fee(amount)
        net_amount = amount - platform_fee
        
        # Create donation
        donation = Donation.objects.create(
            donor=request.user if request.user.is_authenticated else None,
            campaign=campaign,
            amount=amount,
            platform_fee=platform_fee,
            net_amount=net_amount,
            transaction_id=generate_transaction_id('DON'),
            payment_method=data['payment_method'],
            is_anonymous=data.get('is_anonymous', False),
            message=data.get('message', ''),
            donor_name=data.get('donor_name', ''),
            donor_email=data.get('donor_email', ''),
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
        )
        
        # TODO: Initiate payment with payment gateway
        # For now, return payment URL placeholder
        payment_url = f"/payment/{data['payment_method']}/{donation.transaction_id}"
        
        return Response({
            'success': True,
            'data': {
                'donation_id': donation.id,
                'transaction_id': donation.transaction_id,
                'payment_url': payment_url,
                'amount': float(amount),
            }
        }, status=status.HTTP_201_CREATED)


class BkashCallbackView(APIView):
    """Handle bKash payment callback."""
    
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        # TODO: Implement bKash callback logic
        return Response({'success': True, 'message': 'bKash callback received'})


class NagadCallbackView(APIView):
    """Handle Nagad payment callback."""
    
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        # TODO: Implement Nagad callback logic
        return Response({'success': True, 'message': 'Nagad callback received'})


class BkashWebhookView(APIView):
    """Handle bKash webhook."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        # Log webhook
        PaymentWebhook.objects.create(
            gateway='bkash',
            event_type=request.data.get('event_type', 'unknown'),
            payload=request.data,
            headers=dict(request.headers)
        )
        
        # TODO: Process webhook
        return Response({'success': True})


class NagadWebhookView(APIView):
    """Handle Nagad webhook."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        # Log webhook
        PaymentWebhook.objects.create(
            gateway='nagad',
            event_type=request.data.get('event_type', 'unknown'),
            payload=request.data,
            headers=dict(request.headers)
        )
        
        # TODO: Process webhook
        return Response({'success': True})

