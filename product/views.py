from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from product.serializers import ProductSerializer, ProductManagementSerializer
from product.models import Product as ProductModel
from product.permissions import ProductPermission

from user.permissions import AdminOnly

# Create your views here.
class ProductApiView(APIView):
    permission_classes = [ProductPermission]
    def get(self, request):
        products = ProductModel.objects.filter(seller=request.user.id)
        return Response(ProductSerializer(products, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        product_serializer = ProductSerializer(data=request.data)
        if product_serializer.is_valid():
            product_serializer.save(seller=request.user)
            return Response({"message":"상품 업로드 성공!!"}, status=status.HTTP_200_OK)
        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        product = ProductModel.objects.get(id=request.data['product_id'])
        self.check_object_permissions(self.request, product)
        product_serializer = ProductSerializer(product, data=request.data, partial=True)
        if product_serializer.is_valid():
            product_serializer.save()
            return Response({"message":"성공적으로 제품 정보를 수정하였습니다"}, status=status.HTTP_200_OK)
        
        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductManagementApiView(APIView):
    permission_classes = [AdminOnly]
    def get(self, request):
        products = ProductModel.objects.all()
        return Response(ProductManagementSerializer(products, many=True).data, status=status.HTTP_200_OK)
    
    def put(self, request):
        product = ProductModel.objects.get(id=request.data['product_id'])
        product_management_serializer = ProductManagementSerializer(product, data=request.data, partial=True)
        if product_management_serializer.is_valid():
            product_management_serializer.save()
            return Response({"message": "성공적으로 제품 정보를 수정하였습니다"}, status=status.HTTP_200_OK)
        
        return Response(product_management_serializer.errors, status=status.HTTP_400_BAD_REQUEST)