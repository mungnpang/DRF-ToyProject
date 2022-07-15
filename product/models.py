from django.db import models
from user.models import User

# Create your models here.
class Category(models.Model):
    category = models.CharField("카테고리", max_length=20)
    
    def __str__(self):
        return self.category


class Product(models.Model):
    seller = models.ForeignKey(to=User, related_name="product_seller", on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to="static/product/img", blank=True)
    category = models.ManyToManyField(to=Category, related_name="product_category")
    product_description = models.TextField()
    register_date = models.DateTimeField("상품 등록일", auto_now_add=True)
    is_public = models.BooleanField(default=False)
    
    def __str__(self):
        return f'판매자:{self.seller}  상품:{self.product_name}'


class ProductOption(models.Model):
    product = models.ForeignKey(to=Product, related_name="product_option", on_delete=models.CASCADE)
    product_option_detail = models.CharField(max_length=50)
    product_price = models.IntegerField()
    product_amount = models.IntegerField(blank=True)