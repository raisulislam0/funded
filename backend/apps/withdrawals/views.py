"""
Views for withdrawals app.
"""
from rest_framework import generics, permissions
from .models import Withdrawal
from .serializers import WithdrawalSerializer, CreateWithdrawalSerializer


class WithdrawalListView(generics.ListAPIView):
    """List user's withdrawal requests."""
    
    serializer_class = WithdrawalSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Withdrawal.objects.filter(creator=self.request.user)


class WithdrawalDetailView(generics.RetrieveAPIView):
    """Get withdrawal details."""
    
    serializer_class = WithdrawalSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Withdrawal.objects.filter(creator=self.request.user)


class CreateWithdrawalView(generics.CreateAPIView):
    """Create a withdrawal request."""
    
    serializer_class = CreateWithdrawalSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

