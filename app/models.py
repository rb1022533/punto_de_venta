from django.db import models
from django.contrib.auth.models import User


# Create your models here.
    
class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_stock = models.PositiveIntegerField(default=0)
    categoria = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.nombre


class Venta(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    cliente_nombre = models.CharField(max_length=255, blank=True, null=True)
    cliente_telefono = models.CharField(max_length=15, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    productos = models.ManyToManyField(Producto, through='DetalleVenta')

    def __str__(self):
        return f"Venta {self.id} - {self.fecha.strftime('%d/%m/%Y')}"


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
    
    
class Pedido(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    cliente_nombre = models.CharField(max_length=255)
    cliente_telefono = models.CharField(max_length=15)
    direccion = models.TextField()
    fecha_entrega = models.DateField()
    hora_entrega = models.TimeField()
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    productos = models.ManyToManyField(Producto, through='DetallePedido')

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente_nombre}"


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_producto(self):
        return self.cantidad * self.precio_unitario