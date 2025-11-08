from rest_framework import permissions


class IsClient(permissions.BasePermission):
    """
    Permission personnalisée pour vérifier que l'utilisateur est un client
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type == 'client'

