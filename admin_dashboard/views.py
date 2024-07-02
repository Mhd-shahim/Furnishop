from django.shortcuts import render,get_object_or_404
from .models import Banner,Category,Product,Testimonial
from .serializers import BannerSerializer,CategorySerializer,ProductSerializer,TestimonialSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# Create your views here.

@api_view(['GET','POST'])
def banners(request):

    if request.method == 'GET':
        banners = Banner.objects.all()
        serializer = BannerSerializer(banners, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        data = request.data
        serializer = BannerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'message': 'banner created successfully'}, status=status.HTTP_201_CREATED)
        else:
            #return Response({'message': 'Banner creation failed'},status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors)

@api_view(['GET', 'PUT', 'DELETE'])
def bannerMethods(request, pk):
    banner = get_object_or_404(Banner, pk=pk)

    if request.method == 'GET':
        serializer = BannerSerializer(banner)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        data = request.data
        serializer = BannerSerializer(banner, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'message': 'Banner edited successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Banner edit failed'},status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        banner.delete()
        return Response({'message': 'Banner deleted successfully'},status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST']) 
def category(request):

    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        data = request.data
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'message': 'category created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'category creation failed'},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def categoryMethods(request,pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'GET':
        serializer= CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        data = request.data
        serializer = CategorySerializer(category, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'message': 'category edited successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'category edit failed'},status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        category.delete()
        return Response({'message': 'category deleted successfully'},status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def products(request):

    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        data = request.data
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data, 'message':'product created successfully'}, status=status.HTTP_201_CREATED)
        else:
            #return Response({'message': 'product creation failed'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
def productMethods(request,pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        data = request.data
        serializer = ProductSerializer(product, data=data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'message': 'product edited successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors)
        
    elif request.method == 'DELETE':
        product.delete()
        return Response({'message': 'product deleted successfully'},status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def testimonials(request):

     if request.method == 'GET':
         testimonials = Testimonial.objects.all()
         serializer = TestimonialSerializer(testimonials, many=True)
         return Response(serializer.data)
     
     elif request.method == 'POST':
         data = request.data
         serializer = TestimonialSerializer(data=data)
         if serializer.is_valid():
             serializer.save()
             return Response({'data': serializer.data, 'message': 'Testimonial created succcessfully'})
         else:
             return Response(serializer.errors)
         

@api_view(['GET', 'PUT', 'DELETE'])
def testimonialMethods(request,pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)

    if request.method == 'GET':
        serializer = TestimonialSerializer(testimonial)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        data = request.data
        serializer = TestimonialSerializer(testimonial, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'message': 'Testimonial edited successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        testimonial.delete()
        return Response({'message': 'testimonial deleted successfully'},status=status.HTTP_204_NO_CONTENT)
