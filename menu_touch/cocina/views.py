from django.shortcuts import render
from pedidos.models import Pedido  # Importa el modelo Pedido desde la aplicación de pedidos

def vista_cocina(request):
    # Obtén los pedidos en orden de solicitud (por fecha)
    pedidos = Pedido.objects.all().order_by('fecha_pedido')
    
    return render(request, 'cocina/vista_cocina.html', {'pedidos': pedidos})
