"""
Serializers for badges app.
"""
from rest_framework import serializers
from .models import Badge, UserBadge


class BadgeSerializer(serializers.ModelSerializer):
    """Serializer for badges."""
    
    class Meta:
        model = Badge
        fields = ['id', 'name', 'slug', 'description', 'badge_type', 'icon_url', 'color']


class UserBadgeSerializer(serializers.ModelSerializer):
    """Serializer for user badges."""
    
    badge = BadgeSerializer(read_only=True)
    
    class Meta:
        model = UserBadge
        fields = ['id', 'badge', 'earned_at']

