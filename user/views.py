from django.contrib.auth import authenticate, login, logout

from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from user.models import User as UserModel
from user.serializers import UserSerializer, UserManagementSerializer


class UserApiView(APIView):
    def get(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)
    
    def put(self, request):
        user_serializer = UserSerializer(request.user, data=request.data, partial=True)
        
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({"message": "성공적으로 회원정보를 수정하였습니다"}, status=status.HTTP_200_OK)
        
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserJoinApiView(APIView):
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
    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
    
        user = authenticate(request, username=username, password=password)
        
        if not user:
            return Response({"error": "존재하지 않는 계정이거나 패스워드가 일치하지 않습니다"})
        
        login(request, user)
        return Response({"message": "로그인 성공!!"}, status=status.HTTP_200_OK)


class UserLogoutApiView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message":"성공적으로 로그아웃했습니다"}, status=status.HTTP_200_OK)
    
    
class UserManagementApiView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def get(self, request):
        user = UserModel.objects.all()
        return Response(UserSerializer(user, many=True).data, status=status.HTTP_200_OK)
    
    def put(self, request):
        user = UserModel.objects.get(id=request.data['user_id'])
        user_management_serializer = UserManagementSerializer(user, data=request.data, partial=True)
        if user_management_serializer.is_valid():
            user_management_serializer.save()
            return Response({"message":"성공적으로 회원정보를 수정했습니다"}, status=status.HTTP_200_OK)
        
        return Response(user_management_serializer.errors, status=status.HTTP_400_BAD_REQUEST)