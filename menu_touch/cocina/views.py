from django.shortcuts import render
from pedidos.models import Pedido  # Importa el modelo Pedido desde la aplicación de pedidos
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

def vista_cocina(request):
    # Obtén los pedidos en orden de solicitud (por fecha)
    pedidos = Pedido.objects.filter(estado='PREP').order_by('fecha_pedido')
    
    return render(request, 'cocina/vista_cocina.html', {'pedidos': pedidos})

def cambiar_estado_pedido(request, order_id):
    print("Iniciando el proceso para cambiar el estado del pedido...")  # Mensaje inicial

    try:
        # Confirma que el ID de pedido es el correcto
        print(f"Buscando pedido con ID: {order_id}")
        pedido = Pedido.objects.get(id=order_id)
        print(f"Pedido encontrado: {pedido}")

        # Verifica el estado actual del pedido
        print(f"Estado actual del pedido: {pedido.estado}")
        if pedido.estado == 'PREP':
            print("Cambiando el estado del pedido a 'LIST'")
            pedido.estado = 'LIST'  # Cambia el estado a "Listo para entrega"
            pedido.save()
            print("Estado del pedido cambiado y guardado con éxito.")
            return JsonResponse({"success": True})
        else:
            print("El pedido ya está en un estado que no permite el cambio.")
            return JsonResponse({"error": "El pedido ya está listo o entregado"}, status=400)

    except Pedido.DoesNotExist:
        print("Error: Pedido no encontrado")
        return JsonResponse({"error": "Pedido no encontrado"}, status=404)

    except Exception as e:
        print("Error desconocido en cambiar_estado_pedido:", str(e))
        return JsonResponse({"error": "Error interno del servidor"}, status=500)