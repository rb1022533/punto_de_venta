from django.contrib import admin
from .models import Producto, Venta, DetalleVenta, Pedido, DetallePedido

# Registrar tus modelos en el admin
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio_venta', 'cantidad_stock', 'categoria')
    search_fields = ('nombre', 'categoria')

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente_nombre', 'cliente_telefono', 'total', 'fecha')
    search_fields = ('cliente_nombre', 'cliente_telefono')
    list_filter = ('fecha',)

@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ('venta', 'producto', 'cantidad', 'precio_unitario')
    list_filter = ('producto',)
    

class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 1

class PedidoAdmin(admin.ModelAdmin):
    inlines = [DetallePedidoInline]
class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 1

class PedidoAdmin(admin.ModelAdmin):
    inlines = [DetallePedidoInline]

    