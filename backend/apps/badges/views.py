"""
Views for badges app.
"""
from rest_framework import generics, permissions
from .models import Badge, UserBadge
from .serializers import BadgeSerializer, UserBadgeSerializer


class BadgeListView(generics.ListAPIView):
    """List all active badges."""
    
    queryset = Badge.objects.filter(is_active=True)
    serializer_class = BadgeSerializer
    permission_classes = [permissions.AllowAny]


class UserBadgeListView(generics.ListAPIView):
    """List user's earned badges."""
    
    serializer_class = UserBadgeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserBadge.objects.filter(user=self.request.user)

