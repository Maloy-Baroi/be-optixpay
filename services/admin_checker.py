from rest_framework import permissions


class IsSuperAdmin(permissions.BasePermission):
    """
    Custom permission to only allow superadmins to access.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and is a superadmin
        return request.user and request.user.is_authenticated and request.user.is_superuser
