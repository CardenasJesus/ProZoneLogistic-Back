# serializer.py
from rest_framework import serializers
from backProzone.models import Employee, Profile
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'nombre', 'apellido', 'telefono', 'email', 'password', 'status', 'fecha_ingreso', 'user', 'rol', 'departamento']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({'user_id': self.user.id,})

        # Obtener información del empleado
        empleado_data = Employee.objects.filter(user=self.user).values().first()
        if empleado_data:
            data.update({'empleado': empleado_data})

            # Obtener información del perfil del empleado
            perfil_data = Profile.objects.filter(employee__user=self.user).values().first()
            if perfil_data:
                data.update({'perfil': perfil_data})

        return data