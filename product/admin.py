from django.contrib import admin

from product.models import PayMethod as PayMethodModel
from product.models import DeliveryStatus as DeliveryStatusModel
from product.models import Category as CategoryModel
from product.models import Product as ProductModel
from product.models import Review as ReviewModel
from product.models import Cart as CartModel
from product.models import PurchasedList as PurchasedListModel

# Register your models here.
class pay_method_detail(admin.ModelAdmin):
    list_display = ('id', 'pay_method')

class delivery_status_detail(admin.ModelAdmin):
    list_display = ('id', 'delivery_status')

class category_detail(admin.ModelAdmin):
    list_display = ('id', 'category')

class product_detail(admin.ModelAdmin):
    list_display = ('id', 'seller', 'product_name')

class review_detail(admin.ModelAdmin):
    list_display = ('id', 'author', 'product', 'review_content', 'review_rating')

class cart_detail(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'is_present')

class PurchasedList_detail(admin.ModelAdmin):
    list_display = ('id', 'user', 'purchased_item', 'pay_method', 'delivery_status', 'purchased_at', 'is_present')

admin.site.register(PayMethodModel, pay_method_detail)
admin.site.register(DeliveryStatusModel, delivery_status_detail)
admin.site.register(CategoryModel, category_detail)
admin.site.register(ProductModel, product_detail)
admin.site.register(ReviewModel, review_detail)
admin.site.register(CartModel, cart_detail)
admin.site.register(PurchasedListModel, PurchasedList_detail)

