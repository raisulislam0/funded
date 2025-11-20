"""
Views for campaigns app.
"""
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Campaign, CampaignUpdate, CampaignComment
from .serializers import (
    CategorySerializer,
    CampaignListSerializer,
    CampaignDetailSerializer,
    CampaignCreateSerializer,
    CampaignUpdateSerializer,
    CampaignCommentSerializer
)
from apps.core.permissions import IsCampaignCreator, IsVerified


class CategoryListView(generics.ListAPIView):
    """List all active categories."""
    
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class CampaignListView(generics.ListAPIView):
    """List all approved/active campaigns."""
    
    queryset = Campaign.objects.filter(status__in=['approved', 'active'])
    serializer_class = CampaignListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status', 'district']
    search_fields = ['title', 'description', 'short_description']
    ordering_fields = ['created_at', 'goal_amount', 'current_amount']
    ordering = ['-created_at']


class CampaignDetailView(generics.RetrieveAPIView):
    """Get campaign details by slug."""
    
    queryset = Campaign.objects.all()
    serializer_class = CampaignDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


class CampaignCreateView(generics.CreateAPIView):
    """Create a new campaign."""
    
    serializer_class = CampaignCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsVerified]
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user, status='pending')


class CampaignUpdateView(generics.UpdateAPIView):
    """Update campaign (only by creator)."""
    
    queryset = Campaign.objects.all()
    serializer_class = CampaignCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsCampaignCreator]
    lookup_field = 'slug'


class CampaignUpdatesListView(generics.ListAPIView):
    """List all updates for a campaign."""
    
    serializer_class = CampaignUpdateSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        slug = self.kwargs['slug']
        return CampaignUpdate.objects.filter(campaign__slug=slug)


class CreateCampaignUpdateView(generics.CreateAPIView):
    """Create a campaign update (only by creator)."""
    
    serializer_class = CampaignUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        slug = self.kwargs['slug']
        campaign = Campaign.objects.get(slug=slug, creator=self.request.user)
        serializer.save(campaign=campaign)


class CampaignCommentsListView(generics.ListAPIView):
    """List all approved comments for a campaign."""
    
    serializer_class = CampaignCommentSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        slug = self.kwargs['slug']
        return CampaignComment.objects.filter(campaign__slug=slug, is_approved=True)


class CreateCommentView(generics.CreateAPIView):
    """Create a comment on a campaign."""
    
    serializer_class = CampaignCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        slug = self.kwargs['slug']
        campaign = Campaign.objects.get(slug=slug)
        serializer.save(campaign=campaign, user=self.request.user)

