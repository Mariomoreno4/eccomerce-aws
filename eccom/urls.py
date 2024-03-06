from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name='farmacia'),
    
    path('login/',login, name='login'),
    path('registrarse/', register, name="register"),
    path('carrito/',carrito,name='carrito'),
     path('tuorden/',orde,name='orde'),
     path('Confirmacion/',confirmacion,name='confir'),
    path('logout/',exit,name='exit'),
    path('todos/',todo,name='todo'),
    path('buscarps3/', buscar_productops3, name='ps3'),
    path('buscarx360/', buscar_productox360, name='x360'),
    path('buscarwii/', buscar_productowii, name='wii'),
    
    
    



    path('articulo/<int:producto_id> /', detalle_articulo, name='detalle_articulo'),
    path('agregar/<int:producto_id>/', agregar_producto, name="Add"),
    path('eliminar/<int:producto_id>/', eliminar_producto, name="Del"),
    path('restar/<int:producto_id>/', restar_producto, name="Sub"),
    path('limpiar/', limpiar_carrito, name="CLS"),
    
    path('tu perfil/', perfil, name="perfil"),
     path('favoritos/', favorito, name="fav"),
     path('agregar_favorito/<int:producto_id>/', agregar_favorito, name="agregar_favorito"),
    path('eliminar-favorito/<int:producto_id>/', eliminar_favorito, name='eliminar_favorito'),

]
