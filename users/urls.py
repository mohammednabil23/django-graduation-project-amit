from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerUser, name='register'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='login'),
    path('profile/update/', views.updateUserProfile, name='update-profile'),
    path('profile/', views.getUserProfile, name='user-profile'),
    path('', views.getUsers, name='users'),
    path('<int:pk>/delete/', views.deleteUser, name='delete-user'),
    path('<int:pk>/', views.getUserById, name='user-by-id'),
    path('<int:pk>/update/', views.updateUser, name='update-user'),
]