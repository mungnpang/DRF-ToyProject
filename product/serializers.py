from rest_framework import serializers

from django.db.models import Avg

from product.models import Category as CategoryModel
from product.models import Product as ProductModel
from product.models import ProductOption as ProductOptionModel

from user_action.serializers import ReviewSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ["category"]


class ProductOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOptionModel
        fields = ["product_option_detail", "product_price", "product_amount"]


class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True, source='review_set')
    category = CategorySerializer(many=True, required=False)
    product_option = ProductOptionSerializer(many=True, required=False)
    
    class Meta:
        model = ProductModel
        read_only_fields = ["seller"]
        fields = ["seller", "product_name", "category", "product_option", "product_description", "register_date", "is_public", "reviews"]
        
    def create(self, validated_data):
        category = validated_data.pop("category", [])
        product_option = validated_data.pop("product_option", [])
        product = ProductModel(**validated_data)
        product.save()
        
        category_object = CategoryModel.objects.get(category=category[0]["category"])
        product.category.add(category_object)
        
        for option in product_option:
            ProductOptionModel.objects.create(product=product, **option)
        
        return product
        
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
    
    
class ProductManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        read_only_fields = ["seller", "thumbnail", "register_date"]
        fields = "__all__"
        
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance