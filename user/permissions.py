from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_admin == True:
            return True
        return False