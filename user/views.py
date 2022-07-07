from django.contrib.auth import authenticate, login, logout

from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from user.serializers import UserSerializer
from user.models import User as UserModel


class UserApiView(APIView):
    def get(self, request):
        user = UserModel.objects.all()
        return Response(UserSerializer(user, many=True).data, status=status.HTTP_200_OK)


class UserJoinApiView(APIView):
    def get(self, request):
        return Response({"message":"Join get 성공!!"}, status=status.HTTP_200_OK)

    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            if request.data['user_type'] == '판매회원':
                user_serializer.save(is_active=False)
            else:
                user_serializer.save()
            return Response({"message":"가입 완료!"}, status=status.HTTP_200_OK)
        
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class UserLoginApiView(APIView):
    def get(self, request):
        return Response({"message":"Login get 성공!!"}, status=status.HTTP_200_OK)
        
    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
    
        user = authenticate(request, username=username, password=password)
        
        if not user:
            return Response({"error": "존재하지 않는 계정이거나 패스워드가 일치하지 않습니다"})
        
        login(request, user)
        return Response({"message": "로그인 성공!!"}, status=status.HTTP_200_OK)


class UserUpdateApiView(APIView):
    def put(self, request):
        user = request.user
        user_serializer = UserSerializer(user, data=request.data, partial=True)
        
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({"message": "성공적으로 회원정보를 수정하였습니다"}, status=status.HTTP_200_OK)
        
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogout(APIView):
    def post(self, request):
        logout(request)
        return Response({"message":"성공적으로 로그아웃했습니다"}, status=status.HTTP_200_OK)