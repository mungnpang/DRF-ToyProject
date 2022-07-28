from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user_action.permissions import ReviewPermissions, CartPermissions, PurchasedPermissions
from user_action.serializers import ReviewSerializer, CartSerializer, PurchasedListSerializer

from user_action.models import Review as ReviewModel
from user_action.models import Cart as CartModel
from user_action.models import PurchasedList as PurchasedListModel


# Create your views here.
class ReviewApiView(APIView):
    permission_classes = [ReviewPermissions]
    def get(self, request):
        reviews = ReviewModel.objects.filter(product_id=request.GET['product_id'])
        return Response(ReviewSerializer(reviews, many=True).data, status=status.HTTP_200_OK)
    
    def post(self, request):
        review_serializer = ReviewSerializer(data=request.data, partial=True)
        if review_serializer.is_valid():
            review_serializer.save(author=request.user)
            return Response({"message": "성공적으로 상품평을 등록했습니다"}, status=status.HTTP_200_OK)
        return Response(review_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        review = ReviewModel.objects.get(id=request.data['review_id'])        
        self.check_object_permissions(self.request, review)
        review_serializer = ReviewSerializer(review, data=request.data, partial=True)
        if review_serializer.is_valid():
            review_serializer.save()
            return Response({"message": "성공적으로 상품평을 수정했습니다"}, status=status.HTTP_200_OK)
        return Response(review_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        review = ReviewModel.objects.get(id=request.data['review_id'])
        self.check_object_permissions(self.request, review)
        review.delete()
        return Response({"message": "성공적으로 상품평을 삭제했습니다"}, status=status.HTTP_200_OK)


class CartApiView(APIView):
    permission_classes = [CartPermissions]
    def get(self, request):
        carts = CartModel.objects.filter(user_id=request.user.id)
        return Response(CartSerializer(carts, many=True).data, status=status.HTTP_200_OK)
        
    def post(self, request):
        cart_serializer = CartSerializer(data=request.data)
        if cart_serializer.is_valid():
            cart_serializer.save(user=request.user)
            return Response({"message":"성공적으로 장바구니에 담았습니다"}, status=status.HTTP_200_OK)
        return Response(cart_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        cart = CartModel.objects.get(id=request.data['cart_id'])
        self.check_object_permissions(self.request, cart)
        cart_serializer = CartSerializer(cart, data=request.data, partial=True)
        if cart_serializer.is_valid():
            cart_serializer.save()
            return Response({"message":"성공적으로 장바구니 상품을 수정했습니다"}, status=status.HTTP_200_OK)
        return Response(cart_serializer.erros, status=status.HTTP_400_BAD_REQUEST)
    
    
class PurchasedListApiView(APIView):
    permission_classes = [PurchasedPermissions]
    def get(self, request):
        purchased = PurchasedListModel.objects.filter(user_id=request.user.id)
        return Response(PurchasedListSerializer(purchased, many=True).data, status=status.HTTP_200_OK)
    
    def post(self, request):
        purchased_list_serializer = PurchasedListSerializer(data=request.data)
        if purchased_list_serializer.is_valid():
            purchased_list_serializer.save(user=request.user)
            return Response({"message": "구매 완료!"}, status=status.HTTP_200_OK)
        return Response(purchased_list_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        purchased = PurchasedListModel.objects.get(id=request.data['purchased_id'])
        self.check_object_permissions(self.request, purchased)
        purchased_list_serializer = PurchasedListSerializer(purchased, data=request.data, partial=True)
        if purchased_list_serializer.is_valid():
            purchased_list_serializer.save()
            return Response({"message": "성공적으로 구매 상품정보를 수정했습니다"}, status=status.HTTP_200_OK)
        return Response(purchased_list_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    