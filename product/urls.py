from django.urls import path
from product.views import ProductApiView, ReviewApiView, CartApiView, PurchasedListApiView

urlpatterns = [
    path('', ProductApiView.as_view(), name='products'),
    path('upload/', ProductApiView.as_view(), name='upload'),
    path('<obj_id>/', ProductApiView.as_view(), name='product_update'),
    path('<obj_id>/review/', ReviewApiView.as_view(), name='review_upload'),
    path('review/<review_id>/', ReviewApiView.as_view(), name='review_update'),
    path('review/<review_id>/delete/', ReviewApiView.as_view(), name='review_delete'),
    path('<obj_id>/cart/', CartApiView.as_view(), name='cart_in'),
    path('cart/<cart_id>/', CartApiView.as_view(), name='cart_update'),
    path('<obj_id>/purchased/', PurchasedListApiView.as_view(), name='purchased_in'),
    path('purchased/<purchased_id>/', PurchasedListApiView.as_view(), name='purchased_update'),
]