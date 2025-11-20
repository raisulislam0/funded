"""
URL patterns for donations app.
"""
from django.urls import path
from . import views

app_name = 'donations'

urlpatterns = [
    # Donations
    path('', views.DonationListView.as_view(), name='donation_list'),
    path('create/', views.CreateDonationView.as_view(), name='create_donation'),
    path('<uuid:pk>/', views.DonationDetailView.as_view(), name='donation_detail'),
    
    # Payment callbacks
    path('callback/bkash/', views.BkashCallbackView.as_view(), name='bkash_callback'),
    path('callback/nagad/', views.NagadCallbackView.as_view(), name='nagad_callback'),
    
    # Webhooks
    path('webhook/bkash/', views.BkashWebhookView.as_view(), name='bkash_webhook'),
    path('webhook/nagad/', views.NagadWebhookView.as_view(), name='nagad_webhook'),
]

