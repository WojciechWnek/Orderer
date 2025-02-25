from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import ProductSerializer
from api.models import Product

# Django way
def json_product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return JsonResponse({
        "data": serializer.data
    })

def json_product_detail(request, pk):
    product = get_object_or_404(Product, pk = pk)
    serializer = ProductSerializer(product)
    return JsonResponse({
        "data": serializer.data
    })

# Rest Framework way
@api_view(["GET"])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk = pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)
