from django.db.models import Max
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny
)
from rest_framework.views import APIView

from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from api.models import Product, Order, OrderItem


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = "product_id"


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related(
        "items",
        "items__product",
    ).all()
    serializer_class = OrderSerializer


class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related(
        "items",
        "items__product",
    ).all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    # override class bse generic view queryset to match one user
    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        return qs.filter(user=user)


class ProductInfoAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            'products': products,
            'count': len(products),
            "max_price": products.aggregate(maximum_price=Max('price'))['maximum_price']
        })
        return Response(serializer.data)
