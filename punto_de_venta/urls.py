"""
URL configuration for posmart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path
from app import views
from django.urls import reverse_lazy


urlpatterns = [
    path('admin/', admin.site.urls),
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('inicio/', views.inicio, name='inicio'),
    path('logout/', views.cerrar_sesion, name='cerrar_sesion'),
    path('iniciar_sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('cambiar_password/', views.cambiar_password, name='cambiar_password'),
    path('agregar_producto/', views.agregar_producto, name='agregar_producto'), 
    path('lista_productos/', views.lista_productos, name='lista_productos'),
    path('editar_producto/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('eliminar_producto/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('agregar_venta/', views.agregar_venta, name='agregar_venta'),
    path('lista_ventas/', views.lista_ventas, name='lista_ventas'),
    path('detalles_venta/<int:venta_id>/', views.detalles_venta, name='detalles_venta'),
    
]     
 