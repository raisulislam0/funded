"""
Custom permissions for the API.
"""
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner
        return obj.user == request.user


class IsCampaignCreator(permissions.BasePermission):
    """
    Permission to check if user is the campaign creator.
    """
    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission to allow only admins to modify, but anyone to read.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsVerified(permissions.BasePermission):
    """
    Permission to check if user is verified.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_verified

