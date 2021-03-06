from rest_framework import permissions

class ProductPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method == 'POST':
            return bool(user.user_type == 'ํ๋งคํ์' and user.is_active)
        return user.is_authenticated
    
    def has_object_permission(self, request, view, product):
        if product.seller_id == request.user.id:
            return True
        return False