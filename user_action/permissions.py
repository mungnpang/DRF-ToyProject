from rest_framework import permissions
from user.models import User as UserModel

class ReviewPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, review):
        user = request.user
        if request.method in ['PUT','DELETE']:
            author = UserModel.objects.get(id=review.author_id)
            if author == user:
                return True
            return False
        
        return user.is_authenticated


class CartPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, cart):
        user = request.user
        if request.method in ['PUT']:
            if cart.user_id == user.id:
                return True
            return False
        
        return user.is_authenticated


class PurchasedPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, purchased):
        user = request.user
        if request.method in ['PUT']:
            if purchased.user_id == user.id:
                return True
            return False
        
        return user.is_authenticated