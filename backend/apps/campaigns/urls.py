"""
URL patterns for campaigns app.
"""
from django.urls import path
from . import views

app_name = 'campaigns'

urlpatterns = [
    # Categories
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    
    # Campaigns
    path('', views.CampaignListView.as_view(), name='campaign_list'),
    path('create/', views.CampaignCreateView.as_view(), name='campaign_create'),
    path('<slug:slug>/', views.CampaignDetailView.as_view(), name='campaign_detail'),
    path('<slug:slug>/update/', views.CampaignUpdateView.as_view(), name='campaign_update'),
    
    # Campaign Updates
    path('<slug:slug>/updates/', views.CampaignUpdatesListView.as_view(), name='campaign_updates'),
    path('<slug:slug>/updates/create/', views.CreateCampaignUpdateView.as_view(), name='create_update'),
    
    # Comments
    path('<slug:slug>/comments/', views.CampaignCommentsListView.as_view(), name='campaign_comments'),
    path('<slug:slug>/comments/create/', views.CreateCommentView.as_view(), name='create_comment'),
]

