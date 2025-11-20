"""
URL patterns for badges app.
"""
from django.urls import path
from . import views

app_name = 'badges'

urlpatterns = [
    path('', views.BadgeListView.as_view(), name='badge_list'),
    path('my-badges/', views.UserBadgeListView.as_view(), name='user_badges'),
]

