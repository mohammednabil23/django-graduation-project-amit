from django.urls import path
from . import views

urlpatterns = [
    path('', views.getProducts, name='products'),
    path('<int:pk>/', views.getProduct, name='product'),
    path('<int:pk>/delete/', views.deleteProduct, name='delete-product'),
    path('create/', views.createProduct, name='create-product'),
    path('<int:pk>/update/', views.updateProduct, name='update-product'),
    path('<int:pk>/upload/', views.uploadImage, name='upload-image'),
    path('<int:pk>/review/', views.createProductReview, name='create-review'),
]