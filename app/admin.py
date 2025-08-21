from django.contrib import admin
from .models import Producto, Venta, DetalleVenta, Pedido, DetallePedido
# --- Producto ---
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio_venta', 'cantidad_stock', 'categoria')
    search_fields = ('nombre', 'categoria')


# --- Venta ---
@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente_nombre', 'cliente_telefono', 'total', 'fecha')
    search_fields = ('cliente_nombre', 'cliente_telefono')
    list_filter = ('fecha',)


# --- Detalle de Venta ---
@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ('venta', 'producto', 'cantidad', 'precio_unitario')
    list_filter = ('producto',)


# --- Pedido con sus detalles ---
class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 1


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente_nombre', 'cliente_telefono', 'direccion', 'fecha', 'fecha_entrega', 'hora_entrega')
    search_fields = ('cliente_nombre', 'cliente_telefono')
    list_filter = ('fecha', 'fecha_entrega')
    inlines = [DetallePedidoInline]


# --- DetallePedido (si quieres verlo separado también) ---
@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'producto', 'cantidad', 'precio_unitario')
    list_filter = ('producto',)
    