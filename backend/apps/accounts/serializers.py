"""
Serializers for accounts app.
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserVerification, UserProfile

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile."""
    
    class Meta:
        model = UserProfile
        fields = [
            'facebook_url', 'twitter_url', 'linkedin_url', 'website_url',
            'email_notifications', 'sms_notifications', 'newsletter_subscription',
            'total_donations', 'total_campaigns', 'total_raised'
        ]
        read_only_fields = ['total_donations', 'total_campaigns', 'total_raised']


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user model."""
    
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'full_name', 'phone', 'user_type',
            'avatar', 'bio', 'is_verified', 'is_email_verified',
            'is_phone_verified', 'created_at', 'profile'
        ]
        read_only_fields = ['id', 'is_verified', 'is_email_verified', 'is_phone_verified', 'created_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['email', 'full_name', 'phone', 'user_type', 'password', 'password_confirm']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserVerificationSerializer(serializers.ModelSerializer):
    """Serializer for user verification."""
    
    class Meta:
        model = UserVerification
        fields = [
            'id', 'document_type', 'document_number',
            'document_front_url', 'document_back_url', 'selfie_url',
            'address_line', 'city', 'district', 'postal_code',
            'status', 'reviewed_at', 'rejection_reason', 'created_at'
        ]
        read_only_fields = ['id', 'status', 'reviewed_at', 'rejection_reason', 'created_at']


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change."""
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    new_password_confirm = serializers.CharField(required=True, min_length=8)
    
    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError("New passwords do not match.")
        return data

