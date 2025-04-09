from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Review
from .serializers import ProductSerializer, ReviewSerializer

@api_view(['GET'])
def getProducts(request):
    keyword = request.query_params.get('keyword', '')
    products = Product.objects.filter(name__icontains=keyword)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getProduct(request, pk):
    try:
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({'detail': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteProduct(request, pk):
    try:
        product = Product.objects.get(id=pk)
        product.delete()
        return Response({'detail': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Product.DoesNotExist:
        return Response({'detail': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def createProduct(request):
    product = Product.objects.create(
        user=request.user,
        name='Sample Product',
        price=0.00,
        brand='Sample Brand',
        countInStock=0,
        description='',
        category='Sample Category'
    )
    serializer = ProductSerializer(product)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateProduct(request, pk):
    try:
        product = Product.objects.get(id=pk)
        data = request.data
        product.name = data.get('name', product.name)
        product.price = data.get('price', product.price)
        product.brand = data.get('brand', product.brand)
        product.countInStock = data.get('countInStock', product.countInStock)
        product.description = data.get('description', product.description)
        product.category = data.get('category', product.category)
        product.save()
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({'detail': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def uploadImage(request, pk):
    try:
        product = Product.objects.get(id=pk)
        product.image = request.FILES.get('image')
        product.save()
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({'detail': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProductReview(request, pk):
    try:
        product = Product.objects.get(id=pk)
        user = request.user
        data = request.data
        if Review.objects.filter(product=product, user=user).exists():
            return Response({'detail': 'You already reviewed this product'}, status=status.HTTP_400_BAD_REQUEST)
        
        review = Review.objects.create(
            product=product,
            user=user,
            rating=data['rating'],
            comment=data['comment']
        )
        reviews = product.review_set.all()
        product.numReviews = reviews.count()
        product.rating = sum(review.rating for review in reviews) / product.numReviews
        product.save()
        return Response({'detail': 'Review added successfully'}, status=status.HTTP_201_CREATED)
    except Product.DoesNotExist:
        return Response({'detail': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)