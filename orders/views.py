from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem, ShippingAddress
from .serializers import OrderSerializer
from products.models import Product
from django.utils import timezone

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    data = request.data
    if not data.get('orderItems') or len(data['orderItems']) == 0:
        return Response({'detail': 'No order items provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    order = Order.objects.create(
        user=request.user,
        paymentMethod=data['paymentMethod'],
        taxPrice=data['taxPrice'],
        shippingPrice=data['shippingPrice'],
        totalPrice=data['totalPrice']
    )
    ShippingAddress.objects.create(
        order=order,
        address=data['shippingAddress']['address'],
        city=data['shippingAddress']['city'],
        postalCode=data['shippingAddress']['postalCode'],
        country=data['shippingAddress']['country']
    )
    for item in data['orderItems']:
        product = Product.objects.get(id=item['product'])
        OrderItem.objects.create(
            order=order,
            product=product,
            name=product.name,
            qty=item['qty'],
            price=item['price'],
            image=product.image.url if product.image else ''
        )
        product.countInStock -= int(item['qty'])
        product.save()
    
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):
    try:
        order = Order.objects.get(id=pk)
        if request.user == order.user or request.user.is_staff:
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        return Response({'detail': 'Not authorized to view this order'}, status=status.HTTP_403_FORBIDDEN)
    except Order.DoesNotExist:
        return Response({'detail': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOrderToPaid(request, pk):
    try:
        order = Order.objects.get(id=pk)
        if request.user != order.user:
            return Response({'detail': 'Not authorized to update this order'}, status=status.HTTP_403_FORBIDDEN)
        order.isPaid = True
        order.paidAt = timezone.now()
        order.save()
        return Response({'detail': 'Order marked as paid'}, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({'detail': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrders(request):
    orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getAllOrders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateOrderToDelivered(request, pk):
    try:
        order = Order.objects.get(id=pk)
        order.isDelivered = True
        order.deliveredAt = timezone.now()
        order.save()
        return Response({'detail': 'Order marked as delivered'}, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({'detail': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)