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
    fecha_entrega = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'dd/mm/yyyy'
            }
        ),
        input_formats=['%Y-%m-%d'],  # Formato que envía el navegador con type="date"
        required=True,
        label="Fecha de entrega"
    )

    hora_entrega = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                'type': 'time',
                'class': 'form-control'
            }
        ),
        input_formats=['%H:%M'],  # Formato que envía el navegador con type="time"
        required=True,
        label="Hora de entrega"
    )

    class Meta:
        model = Pedido
        fields = ['cliente_nombre', 'cliente_telefono', 'direccion', 'fecha_entrega', 'hora_entrega']
        widgets = {
            'cliente_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'cliente_telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class DetallePedidoForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = ['producto', 'cantidad']
    
        