from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    brand = models.CharField(max_length=200)
    countInStock = models.IntegerField(default=0)
    description = models.TextField()
    category = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    numReviews = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField()
    comment = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.product}"