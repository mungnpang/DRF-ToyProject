from django.urls import path
from product.views import ProductApiView, ProductManagementApiView
from user_action.views import ReviewApiView

urlpatterns = [
    path('', ProductApiView.as_view(), name='products'),
    path('review/', ReviewApiView.as_view(), name='review'),
    path('management/', ProductManagementApiView.as_view(), name='management'),
]
