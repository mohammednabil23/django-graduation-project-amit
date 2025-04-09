from rest_framework import serializers
from .models import Product, Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'rating', 'comment', 'user', 'product', 'createdAt']

class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'brand', 'countInStock', 'description', 
                  'category', 'image', 'rating', 'numReviews', 'user', 'createdAt', 'reviews']