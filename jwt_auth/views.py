from django.http.request import HttpRequest
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.conf import settings
import jwt
from .serializers.common import UserSerializer
from .serializers.populated import PopulatedUserSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers.edit import EditSerializer

User = get_user_model()


class RegisterView(APIView):
    def post(self, request):
        user_to_create = UserSerializer(data=request.data)
        if user_to_create.is_valid():
            user_to_create.save()
            return Response({'message': 'Reg Successful'}, status=status.HTTP_202_ACCEPTED)
        return Response(user_to_create.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user_to_login = User.objects.get(email=email)
        except User.DoesNotExist:
            raise PermissionDenied(detail='Invalid Credentials')
        if not user_to_login.check_password(password):
            raise PermissionDenied(detail='Invalid Credentials')
        dt = datetime.now() + timedelta(days=7)
        token = jwt.encode(
            {'sub': user_to_login.id, 'exp': int(dt.strftime('%s'))},
            settings.SECRET_KEY,
            algorithm='HS256'
        )
        id = user_to_login.id
        username = user_to_login.username
        return Response({'token': token, 'message': f'Welcome back {user_to_login.username}', 'id': id, 'username': username})


class ProfileView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, pk):
        user = User.objects.get(id=pk)
        if user != request.user:
            raise PermissionDenied()
        serialized_user = PopulatedUserSerializer(user)
        return Response(serialized_user.data, status=status.HTTP_200_OK)

    def put(self, request, pk):

        user_to_edit = User.objects.get(id=pk)
        edited_user = EditSerializer(user_to_edit, data=request.data)
        if user_to_edit != request.user:
            raise PermissionDenied()
        if edited_user.is_valid():
            edited_user.save()
            return Response(edited_user.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(edited_user.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ProfileListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serialized_users = PopulatedUserSerializer(users, many=True)
        return Response(serialized_users.data, status=status.HTTP_200_OK)
