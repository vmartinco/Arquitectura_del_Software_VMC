from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('clientes', views.vista_clientes, name='clientes'),
    path('clientes/<int:cliente_id>/', views.detalle_cliente, name='detalle'),

    #URLS PRACTICA 4
    path('clientes/registrar/', views.registrar_cliente, name='registrar_cliente'),
    path('coches/registrar/', views.registrar_coche, name='registrar_coche'),
    path('servicios/registrar/', views.registrar_servicio, name='registrar_servicio'),
    path('coches/buscarCochesByMarca/<str:marca>/', views.buscarCochesByMarca, name='buscarCochesByMarca'),
    path('coches/buscarCochesByMarcaAndCliente/<str:marca>/<int:cliente_id>/', views.buscarCochesByMarcaAndCliente, name='buscarCochesByMarcaAndCliente'),
]