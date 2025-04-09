from rest_framework import serializers
from .models import Order, OrderItem, ShippingAddress

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'name', 'qty', 'price', 'image']

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ['address', 'city', 'postalCode', 'country']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    shipping_address = ShippingAddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'paymentMethod', 'taxPrice', 'shippingPrice', 
                  'totalPrice', 'isPaid', 'paidAt', 'isDelivered', 'deliveredAt', 
                  'createdAt', 'order_items', 'shipping_address']