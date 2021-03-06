from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from accounts.serializers import UserSerializer, LoginSerializer

"""
using drf session authentication

[header]
X-CSRFToken: llhNXa5JtSoF5YRyT7HDhgM9PsxTLQZ9psDU
"""


@api_view(["GET"])
def me(request):
    user = request.user
    if isinstance(user, AnonymousUser):
        return Response(data={"success": False}, status=status.HTTP_200_OK,)
    return Response(
        data={"success": True, **UserSerializer(instance=user).data},
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data["user"]
    auth_login(request, user)
    return Response(UserSerializer(instance=user).data, status=status.HTTP_200_OK)


@api_view(["POST"])
def logout(request):
    auth_logout(request)
    return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
def signup(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    auth_login(request, user)
    return Response(UserSerializer(instance=user).data, status=status.HTTP_201_CREATED)
