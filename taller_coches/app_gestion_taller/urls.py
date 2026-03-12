from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('clientes', views.vista_clientes, name='clientes'),
    path('clientes/<int:cliente_id>/', views.detalle_cliente, name='detalle'),
]