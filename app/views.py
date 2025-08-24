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

from django.contrib import messages

from .forms import ProductoForm, VentaForm, DetalleVentaForm, DetallePedidoForm, PedidoForm
from .models import Venta, Producto, DetalleVenta, Pedido, DetallePedido
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
            form = ProductoForm()  # formulario vacío nuevamente
            return render(request, 'agregar_producto.html', {'form': form})
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
            return redirect('inicio')
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
        
@login_required
@user_passes_test(es_administrador)
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado exitosamente!")
            form = ProductoForm(instance=producto)  # mantener los datos actualizados
            return render(request, 'editar_producto.html', {'form': form, 'producto': producto})
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
    if request.method == "POST":
        # Datos del cliente
        cliente_nombre = request.POST.get('cliente_nombre')
        cliente_telefono = request.POST.get('cliente_telefono')

        # Listas de productos y cantidades
        productos_ids = request.POST.getlist('productos[]')
        cantidades = request.POST.getlist('cantidades[]')

        venta_form = VentaForm(request.POST)
        productos = Producto.objects.filter(cantidad_stock__gt=0)

        if not productos_ids or not cantidades:
            messages.error(request, "Debes agregar al menos un producto")
            return render(request, "agregar_venta.html", {
                "venta_form": venta_form,
                "productos": productos
            })

        # Crear la venta
        venta = Venta.objects.create(
            cliente_nombre=cliente_nombre,
            cliente_telefono=cliente_telefono,
            total=0
        )
        total_venta = 0

        # Agregar detalles de venta
        for pid, cant in zip(productos_ids, cantidades):
            producto = get_object_or_404(Producto, id=pid)
            cantidad = int(cant)

            if producto.cantidad_stock < cantidad:
                messages.error(request, f"No hay suficiente stock de {producto.nombre}")
                venta.delete()
                return render(request, "agregar_venta.html", {
                    "venta_form": venta_form,
                    "productos": productos
                })

            # Reducir stock
            producto.cantidad_stock -= cantidad
            producto.save()

            # Crear detalle de venta
            detalle = DetalleVenta.objects.create(
                venta=venta,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=producto.precio_venta
            )

            total_venta += cantidad * producto.precio_venta

        # Guardar total
        venta.total = total_venta
        venta.save()

        messages.success(request, "Venta registrada exitosamente!")
        # Renderizamos la misma página con formulario vacío
        venta_form = VentaForm()
        return render(request, "agregar_venta.html", {
        "venta_form": VentaForm(),  # formulario vacío
        "productos": Producto.objects.filter(cantidad_stock__gt=0),
})

    else:
        # Formulario vacío
        venta_form = VentaForm()
        productos = Producto.objects.filter(cantidad_stock__gt=0)

        return render(request, "agregar_venta.html", {
            "venta_form": venta_form,
            "productos": productos
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
    # Obtener la venta por ID
    venta = get_object_or_404(Venta, id=venta_id)

    # Construir lista de detalles con subtotal por producto
    detalles_venta = []
    for detalle in venta.detalleventa_set.all():
        detalles_venta.append({
            'detalle': detalle,
            'total_producto': detalle.cantidad * detalle.precio_unitario
        })

    # Pasar todo al template
    return render(request, 'detalles_venta.html', {
        'venta': venta,
        'detalles_venta': detalles_venta,
        'cliente_nombre': venta.cliente_nombre,
        'cliente_telefono': venta.cliente_telefono,
        'fecha': venta.fecha.strftime('%d/%m/%Y %H:%M:%S')
    })
    
    
@login_required
def agregar_pedido(request):
    productos = Producto.objects.filter(cantidad_stock__gt=0)  # productos disponibles

    if request.method == "POST":
        pedido_form = PedidoForm(request.POST)
        productos_ids = request.POST.getlist('productos[]')
        cantidades = request.POST.getlist('cantidades[]')

        if pedido_form.is_valid():
            if not productos_ids or not cantidades:
                messages.error(request, "Debes agregar al menos un producto al pedido")
                return render(request, "agregar_pedido.html", {
                    "pedido_form": pedido_form,
                    "productos": productos
                })

            # Guardar pedido
            pedido = pedido_form.save(commit=False)
            pedido.total = 0
            pedido.save()

            # Guardar detalles y calcular total
            total_pedido = 0
            for pid, cant in zip(productos_ids, cantidades):
                producto = get_object_or_404(Producto, id=pid)
                cantidad = int(cant)

                # Validar stock
                if producto.cantidad_stock < cantidad:
                    messages.error(request, f"No hay suficiente stock de {producto.nombre}")
                    pedido.delete()
                    return render(request, "agregar_pedido.html", {
                        "pedido_form": pedido_form,
                        "productos": productos
                    })

                # Reducir stock
                producto.cantidad_stock -= cantidad
                producto.save()

                # Crear detalle del pedido
                detalle = DetallePedido.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=producto.precio_venta
                )
                total_pedido += cantidad * producto.precio_venta

            # Guardar total final
            pedido.total = total_pedido
            pedido.save()

            # Mensaje de éxito y render en la misma página
            messages.success(request, "Pedido registrado exitosamente!")
            pedido_form = PedidoForm()  # formulario vacío
            return render(request, "agregar_pedido.html", {
                "pedido_form": pedido_form,
                "productos": productos
            })

        else:
            messages.error(request, "Hay errores en el formulario del pedido.")

    else:
        pedido_form = PedidoForm()

    return render(request, "agregar_pedido.html", {
        "pedido_form": pedido_form,
        "productos": productos
    })


@login_required
def lista_pedidos(request):
    pedidos = Pedido.objects.all().order_by('-fecha')
    
    # Construir detalles con subtotal y total por pedido
    pedidos_con_detalle = []
    for pedido in pedidos:
        detalles = []
        total_pedido = 0
        for detalle in pedido.detallepedido_set.all():
            subtotal = detalle.cantidad * detalle.precio_unitario
            total_pedido += subtotal
            detalles.append({
                'detalle': detalle,
                'total_producto': subtotal
            })
        pedidos_con_detalle.append({
            'pedido': pedido,
            'detalles': detalles,
            'total_pedido': total_pedido
        })

    return render(request, 'lista_pedidos.html', {
        'pedidos_con_detalle': pedidos_con_detalle
    })



@login_required
def detalles_pedido(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    detalles = []
    total_pedido = 0

    for detalle in pedido.detallepedido_set.all():
        subtotal = detalle.cantidad * detalle.precio_unitario
        total_pedido += subtotal
        detalles.append({
            'detalle': detalle,
            'total_producto': subtotal
        })

    return render(request, 'detalles_pedido.html', {
        'pedido': pedido,
        'detalles_pedido': detalles,
        'total_pedido': total_pedido
    })
    
@login_required
@user_passes_test(es_administrador)
def eliminar_pedidos(request):
    if request.method == "POST":
        ids = request.POST.getlist('pedidos_ids')
        Pedido.objects.filter(id__in=ids).delete()
        messages.success(request, f"{len(ids)} pedido(s) eliminado(s) exitosamente!")
    return redirect('lista_pedidos')


@login_required
def editar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    productos = Producto.objects.filter(cantidad_stock__gt=0)

    # Detalles existentes para mostrar en la tabla
    detalles_existentes = [
        {
            "producto_id": d.producto.id,
            "nombre": d.producto.nombre,
            "cantidad": d.cantidad,
            "precio_unitario": d.precio_unitario,
            "subtotal": d.cantidad * d.precio_unitario
        }
        for d in pedido.detallepedido_set.all()
    ]

    if request.method == "POST":
        pedido_form = PedidoForm(request.POST, instance=pedido)
        productos_ids = request.POST.getlist('productos[]')
        cantidades = request.POST.getlist('cantidades[]')

        if pedido_form.is_valid():
            pedido_guardado = pedido_form.save(commit=False)

            # Actualizar productos solo si hay datos en la tabla
            if productos_ids and cantidades:
                pedido_guardado.detallepedido_set.all().delete()
                total_pedido = 0
                for pid, cant in zip(productos_ids, cantidades):
                    producto = get_object_or_404(Producto, id=pid)
                    cantidad = int(cant)

                    if producto.cantidad_stock < cantidad:
                        messages.error(request, f"No hay suficiente stock de {producto.nombre}")
                        continue

                    DetallePedido.objects.create(
                        pedido=pedido_guardado,
                        producto=producto,
                        cantidad=cantidad,
                        precio_unitario=producto.precio_venta
                    )
                    total_pedido += cantidad * producto.precio_venta

                pedido_guardado.total = total_pedido
                pedido_guardado.save()
            else:
                # Si no se modifican productos, recalcular total desde detalles existentes
                pedido_guardado.total = sum(
                    d.cantidad * d.precio_unitario for d in pedido_guardado.detallepedido_set.all()
                )
                pedido_guardado.save()

            messages.success(request, "Pedido actualizado exitosamente!")

            # En vez de redirect, volvemos a renderizar para mostrar alert inmediatamente
            return render(request, "agregar_pedido.html", {
                "pedido_form": pedido_form,
                "productos": productos,
                "pedido": pedido,
                "editar": True,
                "detalles_existentes": detalles_existentes
            })

        else:
            messages.error(request, "Hay errores en el formulario del pedido.")

    else:
        pedido_form = PedidoForm(instance=pedido)

    return render(request, "agregar_pedido.html", {
        "pedido_form": pedido_form,
        "productos": productos,
        "pedido": pedido,
        "editar": True,
        "detalles_existentes": detalles_existentes
    })
    
    
@login_required
def eliminar_productos(request):
    if request.method == "POST":
        ids = request.POST.getlist("productos_ids[]")  # recibe lista de IDs desde AJAX
        if ids:
            Producto.objects.filter(id__in=ids).delete()
            messages.success(request, f"{len(ids)} producto(s) eliminado(s) exitosamente.")
        else:
            messages.warning(request, "No seleccionaste ningún producto.")
    return redirect("lista_productos")
    
    
    
    