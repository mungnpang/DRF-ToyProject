from rest_framework import permissions

class ReviewPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, review):
        if review.author_id == request.user.id:
            return True
        return False
    

class CartPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, cart):
        if cart.user_id == request.user.id:
            return True
        return False
        
        
class PurchasedPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, purchased):
        if purchased.user_id == request.user.id:
            return True
        return False