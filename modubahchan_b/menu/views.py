from rest_framework import status
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from .models import *
from mypage.models import *
from mypage.serializers import *
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly

# Create your views here.

@api_view(['GET','POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def product_list_create(request):
    user = request.user
    if request.method == 'GET':
        products = Product.objects.all().order_by('-createDate')
        serializer = ProductListSerializer(products, many=True)
        return Response(data=serializer.data)

    if request.method == 'POST':
        serializer = ProductListSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=user)
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
    
@api_view(['GET','DELETE','PUT'])
@permission_classes([IsAuthenticatedOrReadOnly])
def product_detail_update_delete(request,product_pk):
    product = get_object_or_404(Product, pk=product_pk)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        product.delete()
        data={
            'product_pk':product_pk
        }
        return Response(data,status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = ProductSerializer(instance=product, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def following_product_list(request):
    user = request.user
    followings = user.profile.followings.all()
    productList = []
    if request.method == 'GET':
        for following in followings:
            products = Product.objects.filter(user = following.user)
            userProduct = UserProductSerializer(products, many=True)
            productData = list(userProduct.data)
            for data in productData:
                productList.append(data)
        serializer = sorted(productList, key=lambda k: k.get('createDate',0), reverse=True)
        return Response(serializer)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def search_products(request,word):
    if request.method == 'GET':
        products = Product.objects.filter(name__icontains=word).order_by('-createDate')
        serializer = ProductListSerializer(products, many=True)
        return Response(data=serializer.data)
