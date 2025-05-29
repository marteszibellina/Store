"""PERMISSIONS for API"""

from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Permission class for author or readonly."""

    def has_object_permission(self, request, view, obj):
        """Проверка на автора или администратора."""
        return (request.user == obj.author
                or request.method in permissions.SAFE_METHODS)


class IsReadOnly(permissions.BasePermission):
    """Permission class for readonly."""

    def has_permission(self, request, view):
        """Проверка на readonly."""
        return request.method in permissions.SAFE_METHODS


class IsAuthenticated(permissions.BasePermission):
    """Permission class for authenticated."""

    def has_permission(self, request, view):
        """Проверка на аутентификацию."""
        return request.user.is_authenticated
