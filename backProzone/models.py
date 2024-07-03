from django.db import models
from rest_framework import serializers
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
import datetime

# Create your models here.
class col_departamento(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=100)
    funcion = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre

class col_roles(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=225)
    def __str__(self):
        return self.nombre
        

class Employee(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=10)
    email = models.CharField(max_length=35)
    password = models.CharField(max_length=30)
    status = models.BooleanField(default=True, choices=[(True, 'Activo'), (False, 'Inactivo')])
    fecha_ingreso = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    rol = models.ForeignKey(col_roles, on_delete=models.CASCADE)
    departamento = models.ForeignKey(col_departamento, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Profile(models.Model):
    bio = models.TextField(max_length=500, blank=True, default="Sin información")
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=30, blank=True, default="Tijuana BC")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.employee.nombre

class prd_Almacen(models.Model):
    nombre = models.CharField(max_length=25)
    descripcion = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class prd_contacto_proveedor(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    telefono = models.CharField(max_length=10)
    def __str__(self):
        return self.nombre

class prd_categorias(models.Model):
    nombre_categoria = models.CharField(max_length=25)
    descripcion = models.CharField(max_length=50)
    observaciones = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre_categoria

class prd_producto(models.Model):
    nombre_producto = models.CharField(max_length=20)
    descripcion_producto = models.CharField(max_length=50)
    precio_producto = models.DecimalField(max_digits=5, decimal_places=2)
    vencimiento_producto = models.DateField(null=True, blank=True)
    almacen = models.ForeignKey(prd_Almacen, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre_producto

class prd_lotes(models.Model):
    nombre_lote = models.CharField(max_length=20)
    descripcion_lote = models.CharField(max_length=50)
    existencia_lote = models.IntegerField()
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    precio_lote = models.DecimalField(max_digits=5, decimal_places=2)
    almacen = models.ForeignKey(prd_Almacen, on_delete=models.CASCADE)
    producto = models.ForeignKey(prd_producto, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(prd_contacto_proveedor, on_delete=models.CASCADE)

class prd_producto_catalogo(models.Model):
    producto = models.ForeignKey(prd_producto, on_delete=models.CASCADE)
    categoria = models.ForeignKey(prd_categorias, on_delete=models.CASCADE)
    class Meta:
        unique_together = (('producto', 'categoria'),)
        db_table = 'prd_producto_catalogo'

class pd_clientes(models.Model):
    nombre_cliente = models.CharField(max_length=20)
    apellido_cliente = models.CharField(max_length=20)
    telefono = models.CharField(max_length=12)
    email = models.CharField(max_length=30)
    status = models.BooleanField(default=True, choices=[(True, 'Activo'), (False, 'Inactivo')])
    def __str__(self):
        return self.nombre_cliente

class pd_pedidos(models.Model):
    precio_total = models.DecimalField(max_digits=5, decimal_places=2)
    descripcion = models.CharField(max_length=50)
    fecha_pedido = models.DateField(null=True, blank=True)
    status = models.BooleanField(default=True, choices=[(True, 'Activo'), (False, 'Inactivo')])
    calle = models.CharField(max_length=20)
    num_exterior = models.CharField(max_length=5)
    colonia = models.CharField(max_length=20)
    codigo_postal = models.CharField(max_length=5)
    cliente = models.ForeignKey(pd_clientes, on_delete=models.CASCADE)

    def __str__(self):
        return self.fecha_pedido

class ped_detalles_pedido(models.Model):
    pedido = models.ForeignKey(pd_pedidos, on_delete=models.CASCADE)
    prducto = models.ForeignKey(prd_producto, on_delete=models.CASCADE)
    cantidad= models.CharField(max_length=5)
    precio_cantidad_producto = models.DecimalField(max_digits=5, decimal_places=2)

class env_vehiculos(models.Model):
    marca = models.CharField(max_length=20)
    modelo = models.CharField(max_length=20)
    placas = models.CharField(max_length=10)
    numero_seguro = models.CharField(max_length=20)
    fecha_fabricacion = models.DateField(null=True, blank=True)
    status = models.BooleanField(default=True, choices=[(True, 'Activo'), (False, 'Inactivo')])
    def __str__(self):
        return self.marca

def validar_edad_minima(value):
    if value < 20:
        raise ValidationError('La edad debe ser mayor o igual a 18 años.')

class env_rutas(models.Model):
    origen = models.CharField(max_length=38)
    destino = models.CharField(max_length=38)
    distancia = models.CharField(max_length=10)
    nombre_ruta = models.CharField(max_length=20)
    status = models.BooleanField(default=True, choices=[(True, 'Activo'), (False, 'Inactivo')])
    tiempo_estimado = models.DateField(null=True, blank=True)
    def __str__(self):
        return self.nombre_ruta

class env_tipo_vehiculo(models.Model):
    vehiculo_id = models.ForeignKey('env_vehiculos', on_delete=models.CASCADE)
    nombre_tipo = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=50)
    refigeracion = models.BooleanField(default=False)
    class Meta:
        unique_together = (('vehiculo_id',),)
        db_table = 'env_tipo_vehiculo'

class env_conductores(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    edad = models.IntegerField(validators=[validar_edad_minima])
    genero = models.CharField(max_length=10)
    tipo_licencia = models.CharField(max_length=2, choices=[('B', 'B'), ('C', 'C')])
    numero_licencia = models.CharField(max_length=15)
    status = models.BooleanField(default=True, choices=[(True, 'Activo'), (False, 'Inactivo')])
    def __str__(self):
        return self.nombre

class env_conductores_vehiculos(models.Model):
    conductor_id = models.ForeignKey(env_conductores, on_delete=models.CASCADE)
    vehiculo_id = models.ForeignKey('env_vehiculos', on_delete=models.CASCADE)
    fecha_asignacion = models.DateField(null=True, blank=True)
    fecha_fin_asignacion = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=[('reparacion', 'Reparacion'), ('baja', 'Baja'), ('uso', 'Uso')])
    class Meta:
        unique_together = (('conductor_id', 'vehiculo_id'),)
        db_table = 'env_conductores_vehiculos'

class env_envio(models.Model): 
    descripcion = models.CharField(max_length=50)
    fecha_envio = models.DateField(null=True, blank=True)
    fecha_entrega = models.DateField(null=True, blank=True)
    observaciones = models.CharField(max_length=50)
    status = models.CharField(max_length=15, choices=[('enviado', 'Enviado'), ('en progreso', 'En Progreso'), ('entregado', 'Entregado')])
    ruta = models.ForeignKey(env_rutas, on_delete=models.CASCADE)
    conductor = models.ForeignKey(env_conductores, on_delete=models.CASCADE)
    pedido = models.ForeignKey('pd_pedidos', on_delete=models.CASCADE)
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    def __str__(self):
        return self.descripcion

class env_estado_envio(models.Model):
    observaciones = models.CharField(max_length=50)
    fecha_actualizacion = models.DateField(null=True, blank=True)
    envio_id = models.ForeignKey(env_envio, on_delete=models.CASCADE)

class env_historial_envios(models.Model):
    titulo_historial = models.CharField(max_length=28)
    observaciones = models.CharField(max_length=50)
    fecha_actualizacion = models.DateField(null=True, blank=True)
    envio_id = models.ForeignKey(env_envio, on_delete=models.CASCADE)
    pedido_id = models.ForeignKey('pd_pedidos', on_delete=models.CASCADE)