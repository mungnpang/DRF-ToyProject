from django.contrib import admin
from user_action.models import PayMethod as PayMethodModel
from user_action.models import DeliveryStatus as DeliveryStatusModel
from user_action.models import Review as ReviewModel
from user_action.models import Cart as CartModel
from user_action.models import PurchasedList as PurchasedListModel
# Register your models here.

class pay_method_detail(admin.ModelAdmin):
    list_display = ('id', 'pay_method')

class delivery_status_detail(admin.ModelAdmin):
    list_display = ('id', 'delivery_status')

class review_detail(admin.ModelAdmin):
    list_display = ('id', 'author', 'product', 'review_content', 'review_rating')

class cart_detail(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'is_present')

class PurchasedList_detail(admin.ModelAdmin):
    list_display = ('id', 'user', 'purchased_item', 'pay_method', 'delivery_status', 'purchased_at', 'is_present')


admin.site.register(PayMethodModel, pay_method_detail)
admin.site.register(DeliveryStatusModel, delivery_status_detail)
admin.site.register(ReviewModel, review_detail)
admin.site.register(CartModel, cart_detail)
admin.site.register(PurchasedListModel, PurchasedList_detail)
