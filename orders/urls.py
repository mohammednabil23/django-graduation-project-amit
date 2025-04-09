from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.addOrderItems, name='add-order'),
    path('<int:pk>/', views.getOrderById, name='order-by-id'),
    path('<int:pk>/pay/', views.updateOrderToPaid, name='pay-order'),
    path('myorders/', views.getMyOrders, name='my-orders'),
    path('', views.getAllOrders, name='all-orders'),
    path('<int:pk>/deliver/', views.updateOrderToDelivered, name='deliver-order'),
]