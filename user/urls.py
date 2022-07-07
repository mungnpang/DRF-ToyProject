from django.urls import path
from user.views import UserApiView, UserJoinApiView, UserLoginApiView, UserUpdateApiView, UserLogout

urlpatterns = [
    path('', UserApiView.as_view()),
    path('join/', UserJoinApiView.as_view()),
    path('login/', UserLoginApiView.as_view()),
    path('update/', UserUpdateApiView.as_view()),
    path('logout/', UserLogout.as_view()),
]
