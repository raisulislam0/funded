"""
Serializers for campaigns app.
"""
from rest_framework import serializers
from .models import Category, Campaign, CampaignDocument, CampaignImage, CampaignUpdate, CampaignComment


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for campaign categories."""
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon']


class CampaignDocumentSerializer(serializers.ModelSerializer):
    """Serializer for campaign documents."""
    
    class Meta:
        model = CampaignDocument
        fields = ['id', 'document_type', 'title', 'file_url', 'file_size', 'created_at']


class CampaignImageSerializer(serializers.ModelSerializer):
    """Serializer for campaign images."""
    
    class Meta:
        model = CampaignImage
        fields = ['id', 'image_url', 'caption', 'order']


class CampaignListSerializer(serializers.ModelSerializer):
    """Serializer for campaign list view."""
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    creator_name = serializers.CharField(source='creator.full_name', read_only=True)
    progress_percentage = serializers.FloatField(read_only=True)
    days_remaining = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Campaign
        fields = [
            'id', 'title', 'slug', 'category_name', 'creator_name',
            'short_description', 'cover_image', 'goal_amount', 'current_amount',
            'progress_percentage', 'days_remaining', 'total_donors',
            'status', 'is_featured', 'created_at'
        ]


class CampaignDetailSerializer(serializers.ModelSerializer):
    """Serializer for campaign detail view."""
    
    category = CategorySerializer(read_only=True)
    creator_name = serializers.CharField(source='creator.full_name', read_only=True)
    creator_avatar = serializers.URLField(source='creator.avatar', read_only=True)
    documents = CampaignDocumentSerializer(many=True, read_only=True)
    images = CampaignImageSerializer(many=True, read_only=True)
    progress_percentage = serializers.FloatField(read_only=True)
    days_remaining = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Campaign
        fields = [
            'id', 'title', 'slug', 'category', 'creator_name', 'creator_avatar',
            'short_description', 'description', 'cover_image', 'video_url',
            'goal_amount', 'current_amount', 'currency', 'progress_percentage',
            'start_date', 'end_date', 'days_remaining', 'status', 'is_featured',
            'total_donors', 'total_donations', 'location', 'district',
            'documents', 'images', 'created_at', 'updated_at'
        ]


class CampaignCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating campaigns."""
    
    class Meta:
        model = Campaign
        fields = [
            'title', 'slug', 'category', 'short_description', 'description',
            'cover_image', 'video_url', 'goal_amount', 'start_date', 'end_date',
            'location', 'district'
        ]


class CampaignUpdateSerializer(serializers.ModelSerializer):
    """Serializer for campaign updates."""
    
    class Meta:
        model = CampaignUpdate
        fields = ['id', 'title', 'content', 'image_url', 'created_at']


class CampaignCommentSerializer(serializers.ModelSerializer):
    """Serializer for campaign comments."""
    
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    user_avatar = serializers.URLField(source='user.avatar', read_only=True)
    
    class Meta:
        model = CampaignComment
        fields = ['id', 'user_name', 'user_avatar', 'content', 'created_at']

