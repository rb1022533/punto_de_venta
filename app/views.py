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
    if request.method == 'POST':
        venta_form = VentaForm(request.POST)
        detalle_form = DetalleVentaForm(request.POST)

        if venta_form.is_valid() and detalle_form.is_valid():
            # Guardamos la venta (sin total aún)
            venta = venta_form.save(commit=False)
            venta.total = 0
            venta.save()

            # Procesamos detalle
            producto = detalle_form.cleaned_data['producto']
            cantidad = detalle_form.cleaned_data['cantidad']
            precio_unitario = producto.precio_venta

            # Verificar stock
            if producto.cantidad_stock >= cantidad:
                producto.cantidad_stock -= cantidad
                producto.save()

                # Guardar detalle (usamos el MODELO, no el form)
                detalle = DetalleVenta.objects.create(
                    venta=venta,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=precio_unitario
                )

                # Actualizar total
                venta.total = detalle.cantidad * detalle.precio_unitario
                venta.save()

                messages.success(request, "Venta registrada exitosamente!")
                return redirect('lista_ventas')
            else:
                messages.error(request, "No hay suficiente stock disponible.")
    else:
        venta_form = VentaForm()
        detalle_form = DetalleVentaForm()

    return render(request, 'agregar_venta.html', {
        'venta_form': venta_form,
        'detalle_form': detalle_form
    })
    
    
#Lista ventas    
@login_required
def lista_ventas(request):
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
    
    