from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

from .models import Cliente, Coche, Servicio, CocheServicio

def vista_clientes(request):
    clientes = list(Cliente.objects.values("id", "nombre", "telefono", "email"))
    return JsonResponse(clientes, safe=False)

def detalle_cliente(request, cliente_id):
    try:
        cliente = (Cliente.objects.values("id", "nombre", "telefono", "email")
                                  .get(id=cliente_id))
        return JsonResponse(cliente)
    except Cliente.DoesNotExist:
        return JsonResponse({"error": "Cliente no existente"}, status=404)
