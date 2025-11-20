"""
Views for accounts app.
"""
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import UserVerification
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserVerificationSerializer,
    ChangePasswordSerializer
)
from apps.core.utils import generate_presigned_url

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """User registration endpoint."""
    
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'success': True,
            'message': 'User registered successfully',
            'data': {
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """User login endpoint."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({
                'success': False,
                'error': {'message': 'Email and password are required'}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                'success': False,
                'error': {'message': 'Invalid credentials'}
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.check_password(password):
            return Response({
                'success': False,
                'error': {'message': 'Invalid credentials'}
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.is_active:
            return Response({
                'success': False,
                'error': {'message': 'Account is inactive'}
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'success': True,
            'message': 'Login successful',
            'data': {
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }
        })


class LogoutView(APIView):
    """User logout endpoint."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response({
                'success': True,
                'message': 'Logout successful'
            })
        except Exception as e:
            return Response({
                'success': False,
                'error': {'message': str(e)}
            }, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(generics.RetrieveAPIView):
    """Get current user details."""
    
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class UpdateProfileView(generics.UpdateAPIView):
    """Update user profile."""
    
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    """Change user password."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({
                'success': False,
                'error': {'message': 'Old password is incorrect'}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({
            'success': True,
            'message': 'Password changed successfully'
        })


class SubmitVerificationView(generics.CreateAPIView):
    """Submit identity verification documents."""
    
    serializer_class = UserVerificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VerificationStatusView(APIView):
    """Get verification status."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        try:
            verification = UserVerification.objects.get(user=request.user)
            serializer = UserVerificationSerializer(verification)
            return Response({
                'success': True,
                'data': serializer.data
            })
        except UserVerification.DoesNotExist:
            return Response({
                'success': True,
                'data': None,
                'message': 'No verification submitted yet'
            })


class GeneratePresignedURLView(APIView):
    """Generate presigned URL for file upload."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        file_key = request.data.get('file_key')
        file_type = request.data.get('file_type', 'document')
        
        if not file_key:
            return Response({
                'success': False,
                'error': {'message': 'file_key is required'}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate presigned URL
        presigned_url = generate_presigned_url(file_key)
        
        if not presigned_url:
            return Response({
                'success': False,
                'error': {'message': 'S3 is not configured'}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'success': True,
            'data': {
                'presigned_url': presigned_url,
                'file_key': file_key
            }
        })

