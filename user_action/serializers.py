from rest_framework import serializers

from user.models import User as UserModel

from user_action.models import PayMethod as PayMethodModel
from user_action.models import DeliveryStatus as DeliveryStatusModel
from user_action.models import Review as ReviewModel
from user_action.models import Cart as CartModel
from user_action.models import PurchasedList as PurchasedListModel


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["username"]
        
        
class DeliveryStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryStatusModel
        fields = ["delivery_status"]


class ReviewSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(required=False)
    class Meta:
        model = ReviewModel
        read_only_fields = ["author"]
        fields = ["author", "product", "review_content", "review_rating", "created_at"]

    def create(self, validated_data):
        review = ReviewModel(**validated_data)
        review.save()
        return review
    
    def update(self, instance, validated_data):
        for key,value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartModel
        read_only_fields = ["user"]
        fields = ["user", "product", "is_present"]

    def create(self, validated_data):
        cart = CartModel(**validated_data)
        cart.is_present = True
        cart.save()
        return cart
    
    def update(self, instance, validated_data):
        for key,value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class PurchasedListSerializer(serializers.ModelSerializer):
    delivery_status = DeliveryStatusSerializer(required=False)
    
    class Meta:
        model = PurchasedListModel
        read_only_fields = ["user"]
        fields = ["user", "purchased_item", "pay_method", "delivery_status", "is_present"]
        
    def create(self, validated_data):
        purchased_list = PurchasedListModel(**validated_data)
        purchased_list.delivery_status = DeliveryStatusModel.objects.get(id=1)
        purchased_list.save()
        return purchased_list
    
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key == "pay_method":
                pay_method_object = PayMethodModel.objects.get(pay_method=value)
                setattr(instance, key, pay_method_object)
            if key == "delivery_status":
                delivery_status_object = DeliveryStatusModel.objects.get(delivery_status=value["delivery_status"])
                setattr(instance, key, delivery_status_object) 
            if key == "is_present":
                setattr(instance, key, value)
        instance.save()
        return instance