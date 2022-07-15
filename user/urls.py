from django.urls import path
from user.views import UserApiView, UserJoinApiView, UserLoginApiView, UserLogoutApiView, UserManagementApiView
from user_action.views import CartApiView, PurchasedListApiView


urlpatterns = [
    path('', UserApiView.as_view()),
    path('management/', UserManagementApiView.as_view()),
    path('join/', UserJoinApiView.as_view()),
    path('login/', UserLoginApiView.as_view()),
    path('logout/', UserLogoutApiView.as_view()),
    path('cart/', CartApiView.as_view(), name='cart'),
    path('purchased/', PurchasedListApiView.as_view(), name='purchased'),
]
