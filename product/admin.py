from django.contrib import admin

from product.models import Category as CategoryModel
from product.models import Product as ProductModel


# Register your models here.
class category_detail(admin.ModelAdmin):
    list_display = ('id', 'category')

class product_detail(admin.ModelAdmin):
    list_display = ('id', 'seller', 'product_name')


admin.site.register(CategoryModel, category_detail)
admin.site.register(ProductModel, product_detail)

