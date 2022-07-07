from rest_framework import serializers

from django.db.models import Avg

from product.models import PayMethod as PayMethodModel
from product.models import DeliveryStatus as DeliveryStatusModel
from product.models import Category as CategoryModel

from product.models import Product as ProductModel
from product.models import ProductOption as ProductOptionModel

from product.models import Review as ReviewModel

from product.models import Cart as CartModel
from product.models import PurchasedList as PurchasedListModel

from user.models import User as UserModel


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["username"]
        
        
class PayMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayMethodModel
        fields = ["pay_method"]   


class DeliveryStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryStatusModel
        fields = ["delivery_status"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ["category"]


class ReviewSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(required=False)
    class Meta:
        model = ReviewModel
        read_only_fields = ["author"]
        fields = ["author", "product", "review_content", "review_rating", "created_at"]

    def create(self, validated_data):
        review = ReviewModel(**validated_data)
        review.author = self.context['request'].user
        review.save()
        return review
    
    def update(self, instance, validated_data):
        for key,value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class ProductOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOptionModel
        fields = ["product_option_detail", "product_price", "product_amount"]


class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True, source='review_set')
    category = CategorySerializer(many=True, required=False, source='category_set')
    product_option = ProductOptionSerializer(many=True, required=False)
    
    class Meta:
        model = ProductModel
        read_only_fields = ["seller"]
        fields = ["seller", "product_name", "category", "product_option", "product_description", "register_date", "is_public", "reviews"]
        
    def create(self, validated_data):
        category = validated_data.pop("category", [])
        product_option = validated_data.pop("product_option", [])
        product = ProductModel(**validated_data)
        product.seller = self.context['request'].user
        product.save()
        
        category_object = CategoryModel.objects.get(category=category[0]["category"])
        product.save()
        
        product.category.add(category_object)
        
        for option in product_option:
            ProductOptionModel.objects.create(product=product, **option)
        
        return product
        
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
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
        cart.user = self.context["request"].user
        cart.save()
        return cart
    
    def update(self, instance, validated_data):
        for key,value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class PurchasedListSerializer(serializers.ModelSerializer):
    pay_method = PayMethodSerializer()
    delivery_status = DeliveryStatusSerializer(required=False)
    
    class Meta:
        model = PurchasedListModel
        read_only_fields = ["user"]
        fields = ["user", "purchased_item", "pay_method", "delivery_status", "is_present"]
        
    def create(self, validated_data):
        pay_method_object = PayMethodModel.objects.get(pay_method=validated_data.pop("pay_method")["pay_method"])
        purchased_list = PurchasedListModel(pay_method=pay_method_object, **validated_data)
        purchased_list.delivery_status = DeliveryStatusModel.objects.get(id=1)
        purchased_list.user = self.context["request"].user
        purchased_list.save()
        return purchased_list
    
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key == "pay_method":
                pay_method_object = PayMethodModel.objects.get(pay_method=value["pay_method"])
                setattr(instance, "pay_method", pay_method_object)
            if key == "delivery_status":
                delivery_status_object = DeliveryStatusModel.objects.get(delivery_status=value["delivery_status"])
                setattr(instance, "delivery_status", delivery_status_object) 
            if key == "is_present":
                setattr(instance, "is_present", validated_data["is_present"])
        instance.save()
        return instance