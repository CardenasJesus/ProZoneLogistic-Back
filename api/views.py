# vistas.py
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from backProzone.models import Employee, Profile
from django.contrib.auth.models import User
from .serializer import EmployeeSerializer, ProfileSerializer, UserSerializer, CustomTokenObtainPairSerializer
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.

class EmployeeList(APIView):
    def get(self, request):
        queryset = Employee.objects.all()
        data = EmployeeSerializer(queryset, many=True).data
        return Response(data)

class ProfileList(APIView):
    serializer_class = ProfileSerializer

class UserList(APIView):
    def get(self, request):
        queryset = User.objects.all()
        data = UserSerializer(queryset, many=True).data
        return Response(data)

class EmployeeRegister(generics.CreateAPIView):
    serializer_class = EmployeeSerializer

    def create(self, request, *args, **kwargs):

        user_data = {
            'username': request.data.get('email', ''),  # Usar .get para evitar KeyError
            'email': request.data.get('email', ''),
            'first_name': request.data.get('nombre', ''),
            'last_name': request.data.get('apellido', ''),
            'password': request.data.get('password', '')
        }

        user_serializer = UserSerializer(data=user_data)
        print(user_serializer)
        if user_serializer.is_valid():
            user = user_serializer.save()
            employee_data = request.data.copy()
            employee_data['user'] = user.id
            employee_serializer = self.get_serializer(data=employee_data)
            employee_serializer.is_valid(raise_exception=True)
            self.perform_create(employee_serializer)

            headers = self.get_success_headers(employee_serializer.data)
            return Response(employee_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer