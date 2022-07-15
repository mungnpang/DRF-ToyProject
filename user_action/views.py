from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user_action.serializers import ReviewSerializer, CartSerializer, PurchasedListSerializer

from product.models import Product as ProductModel
from user_action.models import Review as ReviewModel
from user_action.models import Cart as CartModel
from user_action.models import PurchasedList as PurchasedListModel

from user_action.permissions import ReviewPermission, CartPermission, PurchasedPermission

# Create your views here.
class ReviewApiView(APIView):
    permission_classes = [ReviewPermission]
    def get(self, request):
        data = request.data
        reviews = ReviewModel.objects.filter(product_id=data['product_id'])
        return Response(ReviewSerializer(reviews, many=True).data, status=status.HTTP_200_OK)
    
    def post(self, request):
        review_serializer = ReviewSerializer(data=request.data, partial=True)
        
        if review_serializer.is_valid():
            review_serializer.save(author=request.user)
            return Response({"message": "성공적으로 상품평을 등록했습니다"}, status=status.HTTP_200_OK)
        
        return Response(review_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        data = request.data
        review = ReviewModel.objects.get(id=data['review_id'])
        self.check_object_permissions(self.request, review)
        review_serializer = ReviewSerializer(review, data=request.data, partial=True)
        
        if review_serializer.is_valid():
            review_serializer.save()
            return Response({"message": "성공적으로 상품평을 수정했습니다"}, status=status.HTTP_200_OK)

        return Response(review_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        data = request.data
        review = ReviewModel.objects.get(id=request.data['review_id'])
        self.check_object_permissions(self.request, review)
        review.delete()
        return Response({"message": "성공적으로 상품평을 삭제했습니다"}, status=status.HTTP_200_OK)


class CartApiView(APIView):
    permission_classes = [CartPermission]
    def get(self, request):
        user = request.user
        carts = CartModel.objects.filter(user_id=user.id)
        return Response(CartSerializer(carts, many=True).data, status=status.HTTP_200_OK)
        
    def post(self, request):
        cart_serializer = CartSerializer(data=request.data)
        if cart_serializer.is_valid():
            cart_serializer.save(user=request.user)
            return Response({"message":"성공적으로 장바구니에 담았습니다"}, status=status.HTTP_200_OK)
        
        return Response(cart_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        data = request.data
        cart = CartModel.objects.get(id=data['cart_id'])
        self.check_object_permissions(self.request, cart)
        cart_serializer = CartSerializer(cart, data=request.data, partial=True)
        
        if cart_serializer.is_valid():
            cart_serializer.save()
            return Response({"message":"성공적으로 장바구니 상품을 수정했습니다"}, status=status.HTTP_200_OK)

        return Response(cart_serializer.erros, status=status.HTTP_400_BAD_REQUEST)
    
    
class PurchasedListApiView(APIView):
    permission_classes = [PurchasedPermission]
    def get(self, request):
        user = request.user
        purchased = PurchasedListModel.objects.filter(user_id=user.id)
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