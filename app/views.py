from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required, user_passes_test # PROTEGER RUTAS

from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from .forms import ProductoForm, VentaForm
from django.contrib import messages
from django.shortcuts import render

from .forms import ProductoForm, VentaForm, DetalleVentaForm
from .models import Venta, Producto, DetalleVenta
from django.forms import inlineformset_factory


# Create your views here.
def es_administrador(user):
    return user.is_superuser

@login_required  # Asegura que el usuario esté autenticado
@user_passes_test(es_administrador)  # Asegura que solo los administradores puedan acceder
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto agregado exitosamente!")
            return redirect('lista_productos')  # Redirige a la lista de productos
    else:
        form = ProductoForm()

    return render(request, 'agregar_producto.html', {'form': form})

# Cambiar contraseña
@login_required
def cambiar_password(request):
    if request.method == 'GET':
        return render(request, 'cambiar_password.html', {'form': PasswordChangeForm(user=request.user)})
    else:
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Mantener la sesión activa
            messages.success(request, 'Tu contraseña se cambió con éxito')  # Mensaje de éxito
            return redirect('inicio')  # Redirigir al inicio
        else:
            return render(request, 'cambiar_password.html', {'form': form, 'error': 'Las contraseñas no coinciden o son inválidas'})

 
# Crear_usuario (Crear nuevo usuario)
@login_required
def crear_usuario(request):
    if request.method == 'GET':
      return render(request, 'crear_usuario.html', {'form': UserCreationForm()})
    else: 
        if request.POST['password1'] == request.POST['password2']:
           try:
             #Registrar usuario
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
            user.save()
            login(request, user)
            return redirect('tareas')
           except IntegrityError:
               return render(request, 'crear_usuario.html', {'form': UserCreationForm(), "error": 'El usuario ya existe'})
        return render(request, 'crear_usuario.html', {'form': UserCreationForm(), "error": 'Las contraseñas no coinciden'})          
    
#Inicio
@login_required
def inicio(request):        
    return render(request, 'inicio.html')


#logout(cerrar sesión) 
@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('iniciar_sesion')
 
#login (singin) Entrar a la sesión ya creada.
def iniciar_sesion(request):
    if request.method == 'GET':
      return render(request, 'iniciar_sesion.html', {'form': AuthenticationForm})
    else: 
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
         return render(request, 'iniciar_sesion.html', {'form': AuthenticationForm, 'error': 'Usuario y/o contraseña incorrecto.'})   
        else:
            login(request, user)
            return redirect('inicio')           
        

# Agregar producto  
@login_required
@user_passes_test(es_administrador)      
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'agregar_producto.html', {'form': form})

@login_required
@user_passes_test(es_administrador)
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado exitosamente!")
            return redirect('lista_productos')  # Redirige a la lista de productos
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'editar_producto.html', {'form': form, 'producto': producto})

@login_required
def lista_productos(request):
    productos = Producto.objects.all()  # Obtener todos los productos
    return render(request, 'lista_productos.html', {'productos': productos})

@login_required
@user_passes_test(es_administrador)
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, "Producto eliminado exitosamente!")
        return redirect('lista_productos')  # Redirige a la lista de productos

    return render(request, 'eliminar_producto.html', {'producto': producto})

#Agregar Venta
@login_required
def agregar_venta(request):
    DetalleVentaFormSet = inlineformset_factory(
        Venta, DetalleVenta,
        form=DetalleVentaForm,
        extra=1,  # número inicial de formularios
        can_delete=True
    )

    if request.method == 'POST':
        venta_form = VentaForm(request.POST)
        formset = DetalleVentaFormSet(request.POST)

        if venta_form.is_valid() and formset.is_valid():
            venta = venta_form.save(commit=False)
            venta.total = 0
            venta.save()

            total_venta = 0
            for form in formset:
                if form.cleaned_data:  # evita errores con formularios vacíos
                    detalle = form.save(commit=False)
                    detalle.venta = venta

                    if detalle.producto.cantidad_stock >= detalle.cantidad:
                        detalle.producto.cantidad_stock -= detalle.cantidad
                        detalle.producto.save()

                        detalle.precio_unitario = detalle.producto.precio_venta
                        detalle.save()

                        total_venta += detalle.cantidad * detalle.precio_unitario
                    else:
                        messages.error(request, f"No hay suficiente stock de {detalle.producto.nombre}")

            venta.total = total_venta
            venta.save()

            messages.success(request, "Venta registrada exitosamente!")
            return redirect('lista_ventas')
    else:
        venta_form = VentaForm()
        formset = DetalleVentaFormSet()

    return render(request, 'agregar_venta.html', {
        'venta_form': venta_form,
        'formset': formset
    })
    
    
#Lista ventas    
@login_required
def lista_ventas(request):
    # Obtenemos todas las ventas, ordenadas por fecha descendente
    ventas = Venta.objects.all().order_by('-fecha')
    return render(request, 'lista_ventas.html', {'ventas': ventas})

#Detalles de venta
@login_required
def detalles_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)

    detalles_venta = []
    for detalle in venta.detalleventa_set.all():
        total_producto = detalle.cantidad * detalle.precio_unitario
        detalles_venta.append({
            'detalle': detalle,
            'total_producto': total_producto
        })

    return render(request, 'detalles_venta.html', {
        'venta': venta,
        'detalles_venta': detalles_venta,
        'cliente_nombre': venta.cliente_nombre,
        'cliente_telefono': venta.cliente_telefono,
        'fecha': venta.fecha.strftime('%d/%m/%Y %H:%M:%S')
    })
    
    