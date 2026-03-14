from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import Cliente, Coche, Servicio, CocheServicio

def vista_clientes(request):
    #VISTA ANTIGUA SIN TEMPLATES
    #clientes = list(Cliente.objects.values("id", "nombre", "telefono", "email"))
    #return JsonResponse(clientes, safe=False)
    # VISTA ANTIGUA CON TEMPLATES
    clientes = Cliente.objects.all()
    return render(request, 'app_gestion_taller/lista_clientes.html',
                  {'clientes': clientes})

def detalle_cliente(request, cliente_id):
    # VISTA ANTIGUA SIN TEMPLATES
#    try:
#        cliente = (Cliente.objects.values("id", "nombre", "telefono", "email")
#                                  .get(id=cliente_id))
#        return JsonResponse(cliente)
#    except Cliente.DoesNotExist:
#        return JsonResponse({"error": "Cliente no existente"}, status=404)
    # VISTA ANTIGUA CON TEMPLATES
    try:
        cliente = Cliente.objects.get(id=cliente_id)
        coches = Coche.objects.filter(cliente=cliente)
        contexto = {
            'cliente': cliente,
            'coches': coches,
        }
        return render(request, 'app_gestion_taller/detalle_cliente.html', contexto)
    except Cliente.DoesNotExist:
        return JsonResponse({"error": "Cliente no encontrado"}, status=404)

def detalleCocheServicio(request, coche_id):
    try:
        coche = Coche.objects.get(id=coche_id)
        cocheServicio = CocheServicio.objects.filter(coche=coche)
        contexto = {
            'coche': coche,
            'cocheServicio': cocheServicio,
        }
        return render(request, 'app_gestion_taller/detalle_coche_servicio.html', contexto)
    except CocheServicio.DoesNotExist:
        return JsonResponse({"error": "El Coche no tiene servicios"}, status=404)

#PRACTICA 4

@csrf_exempt
def registrar_cliente(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cliente = Cliente.objects.create(
                nombre=data['nombre'],
                telefono=data['telefono'],
                email=data['email']
            )

            return JsonResponse({"mensaje": "Cliente registrado con éxito", "cliente_id": cliente.id})

        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def registrar_coche(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cliente = Cliente.objects.get(id=data['cliente_id'])
            coche = Coche.objects.create(
                cliente=cliente,
                marca=data['marca'],
                modelo=data['modelo'],
                matricula=data['matricula']
            )
            return JsonResponse({"mensaje": "Coche registrado con éxito", "coche_id": coche.id})

        except Cliente.DoesNotExist:
            return JsonResponse({"error": "Cliente no encontrado"}, status=404)
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def registrar_servicio(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            coche = Coche.objects.get(id=data['coche_id'])
            servicio = Servicio.objects.create(
                nombre=data['nombre'],
                descripcion=data['descripcion']
            )
            CocheServicio.objects.create(coche=coche, servicio=servicio)
            return JsonResponse({"mensaje": "Servicio registrado con éxito",
                                 "servicio_id": servicio.id})

        except Coche.DoesNotExist:
            return JsonResponse({"error": "Coche no encontrado"}, status=404)
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)

def buscarCochesByMarca(request, marca):
    try:
        coches = list(Coche.objects.filter(marca=marca).values("modelo"))
        return JsonResponse(coches, safe=False)

    except Coche.DoesNotExist:
        return JsonResponse({"error": "Coche no encontrado"}, status=404)

def buscarCochesByMarcaAndCliente(request, marca, cliente_id):
    try:
        coches = list(Coche.objects.filter(marca=marca, cliente_id=cliente_id).values("marca", "modelo", "matricula"))
        return JsonResponse(coches, safe=False)

    except Coche.DoesNotExist:
        return JsonResponse({"error": "Coche no encontrado"}, status=404)