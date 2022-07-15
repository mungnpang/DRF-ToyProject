from rest_framework import permissions

class ProductPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method == 'POST':
            return bool(user.user_type == '판매회원' and user.is_active)
        return user.is_authenticated
                
    def has_object_permission(self, request, view, product):
        user = request.user
        if product.seller_id == user.id:
            return True
        return False