from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from product.serializers import ProductSerializer, ReviewSerializer, CartSerializer, PurchasedListSerializer

from product.models import Product as ProductModel
from product.models import Review as ReviewModel
from product.models import Cart as CartModel
from product.models import PurchasedList as PurchasedListModel

from user.models import User as UserModel

# Create your views here.
class ProductPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method == 'GET':
            return user.is_authenticated
        
        if request.method == 'POST':
            return bool(user.user_type == '판매회원' and user.is_active)
        
    def has_object_permission(self, request, view, product):
        user = request.user
        if product.seller_id == user.id:
            return True
        return False
    
    
class ReviewPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, review):
        user = request.user
        if request.method in ['GET','POST']:
            return user.is_authenticated
        
        if request.method in ['PUT','DELETE']:
            author = UserModel.objects.get(id=review.author_id)
            if author == user:
                return True
            return False


class CartPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, cart):
        user = request.user
        if request.method in ['GET', 'POST']:
            return user.is_authenticated
        
        if request.method in ['PUT']:
            if cart.user_id == user.id:
                return True
            return False


class PurchasedPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, purchased):
        user = request.user
        if request.method in ['GET', 'POST']:
            return user.is_authenticated
        
        if request.method in ['PUT']:
            if purchased.user_id == user.id:
                return True
            return False


class ProductApiView(APIView):
    permission_classes = [ProductPermission]
    def get(self, request):
        print(request.method)
        products = ProductModel.objects.all().order_by('?')
        return Response(ProductSerializer(products, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        product_serializer = ProductSerializer(data=request.data, context={"request": request})
        if product_serializer.is_valid():
            product_serializer.save()
            return Response({"message":"상품 업로드 성공!!"}, status=status.HTTP_200_OK)
        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, obj_id):
        product = ProductModel.objects.get(id=obj_id)
        self.check_object_permissions(self.request, product)
        product_serializer = ProductSerializer(product, data=request.data, partial=True)

        if product_serializer.is_valid():
            product_serializer.save()
            return Response({"message":"성공적으로 제품 정보를 수정하였습니다"}, status=status.HTTP_200_OK)
        
        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ReviewApiView(APIView):
    permission_classes = [ReviewPermission]
    def get(self, request, review_id):
        reviews = ReviewModel.objects.filter(id=review_id)
        return Response(ReviewSerializer(reviews, many=True).data, status=status.HTTP_200_OK)
    
    def post(self, request, obj_id):
        data = request.data.dict()
        data['product'] = obj_id
        review_serializer = ReviewSerializer(data=data, context={"request": request})
        
        if review_serializer.is_valid():
            review_serializer.save()
            return Response({"message": "성공적으로 상품평을 등록했습니다"}, status=status.HTTP_200_OK)
        
        return Response(review_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, review_id):
        review = ReviewModel.objects.get(id=review_id)
        self.check_object_permissions(self.request, review)
        review_serializer = ReviewSerializer(review, data=request.data, partial=True)
        
        if review_serializer.is_valid():
            review_serializer.save()
            return Response({"message": "성공적으로 상품평을 수정했습니다"}, status=status.HTTP_200_OK)

        return Response(review_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, review_id):
        review = ReviewModel.objects.get(id=review_id)
        self.check_object_permissions(self.request, review)
        review.delete()
        return Response({"message": "성공적으로 상품평을 삭제했습니다"}, status=status.HTTP_200_OK)


class CartApiView(APIView):
    permission_classes = [CartPermission]
    def get(self, request, obj_id):
        carts = CartModel.objects.filter(product_id=obj_id)
        return Response(CartSerializer(carts, many=True).data, status=status.HTTP_200_OK)
        
    def post(self, request, obj_id):
        request.data['product'] = obj_id
        cart_serializer = CartSerializer(data=request.data, context={"request":request})
        
        if cart_serializer.is_valid():
            cart_serializer.save()
            return Response({"message":"성공적으로 장바구니에 담았습니다"}, status=status.HTTP_200_OK)
        
        return Response(cart_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, cart_id):
        cart = CartModel.objects.get(id=cart_id)
        self.check_object_permissions(self.request, cart)
        cart_serializer = CartSerializer(cart, data=request.data, partial=True)
        
        if cart_serializer.is_valid():
            cart_serializer.save()
            return Response({"message":"성공적으로 장바구니 상품을 수정했습니다"}, status=status.HTTP_200_OK)

        return Response(cart_serializer.erros, status=status.HTTP_400_BAD_REQUEST)
    
    
class PurchasedListApiView(APIView):
    permission_classes = [PurchasedPermission]
    def get(self, request, obj_id):
        purchased = PurchasedListModel.objects.filter(purchased_item_id=obj_id)
        return Response(PurchasedListSerializer(purchased, many=True).data, status=status.HTTP_200_OK)
    
    def post(self, request, obj_id):
        request.data["purchased_item"] = obj_id
        purchased_list_serializer = PurchasedListSerializer(data=request.data, context={"request":request})
        
        if purchased_list_serializer.is_valid():
            purchased_list_serializer.save()
            return Response({"message": "구매 완료!"}, status=status.HTTP_200_OK)
        
        return Response(purchased_list_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, purchased_id):
        purchased = PurchasedListModel.objects.get(id=purchased_id)
        self.check_object_permissions(self.request, purchased)
        purchased_list_serializer = PurchasedListSerializer(purchased, data=request.data, partial=True)
        
        if purchased_list_serializer.is_valid():
            purchased_list_serializer.save()
            return Response({"message": "성공적으로 구매 상품정보를 수정했습니다"}, status=status.HTTP_200_OK)

        return Response(purchased_list_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
