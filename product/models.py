from django.db import models
from user.models import User

# Create your models here.
class PayMethod(models.Model):
    pay_method = models.CharField("결제 수단", max_length=10)
    
    def __str__(self):
        return self.pay_method


class DeliveryStatus(models.Model):
    delivery_status = models.CharField("배송 정보", max_length=10)
    
    def __str__(self):
        return self.delivery_status
    

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
    
    
class Review(models.Model):
    author = models.ForeignKey(to=User, verbose_name="리뷰 작성자", related_name="review_author", on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, verbose_name="상품", related_name="review_product", on_delete=models.CASCADE)
    review_content = models.TextField("리뷰 내용")
    review_rating = models.IntegerField("평점")
    created_at = models.DateTimeField("리뷰 작성일", auto_now_add=True)


class Cart(models.Model):
    user = models.ForeignKey(to=User, related_name="cart_user", on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, related_name="cart_product", on_delete=models.CASCADE)
    is_present = models.BooleanField(default=True)


class PurchasedList(models.Model):
    user = models.ForeignKey(to=User, verbose_name="사용자", related_name="purchased_user", on_delete=models.CASCADE)
    purchased_item = models.ForeignKey(to=Product, verbose_name="제품명", related_name="purchased_item", on_delete=models.CASCADE)
    purchased_at = models.DateTimeField("구매 일자", auto_now_add=True)
    pay_method = models.ForeignKey(to=PayMethod, on_delete=models.CASCADE)
    delivery_status = models.ForeignKey(to=DeliveryStatus, related_name="purchased_item_delivery_status", on_delete=models.CASCADE)
    is_present = models.BooleanField(default=True)
    