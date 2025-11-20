"""
URL patterns for accounts app.
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    # User profile
    path('me/', views.CurrentUserView.as_view(), name='current_user'),
    path('me/update/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('me/change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    
    # Verification
    path('verification/submit/', views.SubmitVerificationView.as_view(), name='submit_verification'),
    path('verification/status/', views.VerificationStatusView.as_view(), name='verification_status'),
    
    # Presigned URLs for document upload
    path('upload/presigned-url/', views.GeneratePresignedURLView.as_view(), name='presigned_url'),
]

