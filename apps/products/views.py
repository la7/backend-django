from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .services import ProductService
from .serializers import ProductSerializer

class ProductListCreateView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ProductService()

    @extend_schema(responses=ProductSerializer(many=True))
    def get(self, request):
        products = self.service.get_all_products()
        return Response(products, status=status.HTTP_200_OK)

    @extend_schema(request=ProductSerializer, responses=ProductSerializer)
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_product = self.service.create_product(serializer.validated_data)
        return Response(new_product, status=status.HTTP_201_CREATED)

class ProductDetailView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ProductService()

    @extend_schema(responses=ProductSerializer)
    def get(self, request, pk):
        product = self.service.get_product_by_id(pk)
        return Response(product, status=status.HTTP_200_OK)

    @extend_schema(request=ProductSerializer, responses=ProductSerializer)
    def put(self, request, pk):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_product = self.service.update_product(pk, serializer.validated_data)
        return Response(updated_product, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        self.service.delete_product(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)