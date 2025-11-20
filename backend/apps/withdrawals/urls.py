"""
URL patterns for withdrawals app.
"""
from django.urls import path
from . import views

app_name = 'withdrawals'

urlpatterns = [
    path('', views.WithdrawalListView.as_view(), name='withdrawal_list'),
    path('create/', views.CreateWithdrawalView.as_view(), name='create_withdrawal'),
    path('<uuid:pk>/', views.WithdrawalDetailView.as_view(), name='withdrawal_detail'),
]

