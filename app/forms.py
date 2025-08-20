from django.forms import ModelForm
from django import forms
from .models import Producto, Venta, DetalleVenta

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

    
        