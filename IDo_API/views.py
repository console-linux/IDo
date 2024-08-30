import django.contrib.auth.models
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import UserSerializer
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        new_user = serializer.save()
        login(request, new_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def log_in(request):
    try:
        User.objects.get(username=request.data['username'], password=request.data['password'])
    except django.contrib.auth.models.User.DoesNotExist:
        return Response(status.HTTP_401_UNAUTHORIZED)
    else:
        login(request, User.objects.get(username=request.data['username'], password=request.data['password']))
        return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def log_out(request):
    if request.user.is_authenticated:
        logout(request)
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['PUT'])
def edit_user(request):
    if request.user.is_authenticated:
        user = request.user
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def get_user(request):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    else:
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

@api_view(['DELETE'])
@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return Response(status=status.HTTP_200_OK)