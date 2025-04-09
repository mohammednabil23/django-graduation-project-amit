from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserSerializer, UserProfileSerializer
from .models import UserProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        UserProfile.objects.create(user=user)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    # Handled by MyTokenObtainPairView in urls.py
    pass

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    data = request.data
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    if data.get('password'):
        user.set_password(data['password'])
    user.save()
    
    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.bio = data.get('bio', profile.bio)
    profile.address = data.get('address', profile.address)
    profile.save()
    
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
    try:
        user = User.objects.get(id=pk)
        user.delete()
        return Response({'detail': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request, pk):
    try:
        user = User.objects.get(id=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateUser(request, pk):
    try:
        user = User.objects.get(id=pk)
        data = request.data
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.is_staff = data.get('isAdmin', user.is_staff)
        if data.get('password'):
            user.set_password(data['password'])
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)