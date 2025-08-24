from django.forms import ModelForm
from django import forms
from .models import Producto, Venta, DetalleVenta, Pedido, DetallePedido

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio_venta', 'cantidad_stock', 'categoria']  


class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente_nombre', 'cliente_telefono']  # 👈 ya no pedimos cliente FK


class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['producto', 'cantidad']
        
class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente_nombre', 'cliente_telefono', 'direccion', 'fecha_entrega', 'hora_entrega']
        widgets = {
            'fecha_entrega': forms.DateInput(attrs={'type': 'date'}),
            'hora_entrega': forms.TimeInput(attrs={'type': 'time'}),
        }

class DetallePedidoForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = ['producto', 'cantidad']
    
        