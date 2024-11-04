from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Mesa, Pedido, PedidoProducto
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import JsonResponse
from django.db.models import F
import json
from django.views.decorators.csrf import csrf_exempt

def home(request):
    mesa_token = request.session.get('mesa_token', None)
    mesa_nombre = mesa_token.split('_')[0] if mesa_token else "Desconocida"
    return render(request, 'home.html', {'mesa_nombre': mesa_nombre})

def mesa_login(request):
    if request.method == 'POST':
        # Validación del login de la mesa
        mesa_nombre = request.POST.get('mesa_nombre')
        mesa_password = request.POST.get('mesa_password')
        
        # Verificar credenciales
        if mesa_nombre == "mesa1" and mesa_password == "nintendo1":
            # Crear el token y guardarlo en la sesión
            mesa_token = f"{mesa_nombre}_token"
            request.session['mesa_token'] = mesa_token
            return redirect('home')  # Redirige al home después del login exitoso
        else:
            # Mensaje de error si las credenciales son incorrectas
            return render(request, 'login.html', {'error': 'Credenciales incorrectas.'})
    
    return render(request, 'login.html')

# CATEGORIAS
def categorias(request):
    # Obtener el nombre de la mesa desde la sesión
    mesa_token = request.session.get('mesa_token', None)
    mesa_nombre = mesa_token.split('_')[0] if mesa_token else "Desconocida"

    categorias_disponibles = [
        {'nombre': 'Platos', 'imagen': '/media/platos.jpg'},
        {'nombre': 'Bebestibles', 'imagen': '/media/bebestibles.jpg'},
        {'nombre': 'Acompañamiento', 'imagen': '/media/acompañamiento.jpg'},
        {'nombre': 'Postres', 'imagen': '/media/postres.jpg'},
    ]

    context = {
        'categorias': categorias_disponibles,
        'mesa_nombre': mesa_nombre,  # Agregar mesa_nombre al contexto
    }
    return render(request, 'categorias.html', context)


# MENU
def menu(request):
    mesa_token = request.session.get('mesa_token', None)
    mesa_nombre = mesa_token.split('_')[0] if mesa_token else "Desconocida"

    # Obtener categoría seleccionada de los parámetros GET
    categoria = request.GET.get('categoria')
    if categoria:
        productos = Producto.objects.filter(categoria=categoria)
    else:
        productos = Producto.objects.all()

    return render(request, 'menu.html', {
        'productos': productos,
        'mesa_nombre': mesa_nombre,
        'categoria_seleccionada': categoria
    })

# PEDIR
def agregar_pedido(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            print('Datos recibidos:', data)  # Verifica los datos recibidos
            
            carrito = data.get('carrito', [])
            
            if not carrito:
                return JsonResponse({'error': 'El carrito está vacío'}, status=400)
            
            # Obtener el nombre de la mesa desde la sesión o derivar de mesa_token
            mesa_nombre = request.session.get('mesa_nombre')
            if not mesa_nombre:
                mesa_token = request.session.get('mesa_token')
                if mesa_token:
                    mesa_nombre = mesa_token.split('_')[0]  # Extrae el nombre de la mesa del token
                    print("Mesa nombre derivado de mesa_token:", mesa_nombre)
            
            print("Mesa nombre desde la sesión:", mesa_nombre)
            
            if not mesa_nombre:
                print("Sesión actual:", request.session.items())
                return JsonResponse({'error': 'Mesa no encontrada en la sesión'}, status=400)

            # Verificar si la mesa existe en la base de datos
            try:
                mesa = Mesa.objects.get(username=mesa_nombre)
            except Mesa.DoesNotExist:
                return JsonResponse({'error': 'Mesa no encontrada en la base de datos'}, status=404)

            # Crear pedido y procesar productos
            pedido = Pedido.objects.create(mesa=mesa, total=0)
            total_pedido = 0
            
            for item in carrito:
                try:
                    producto = Producto.objects.get(id=item['id'])
                except Producto.DoesNotExist:
                    return JsonResponse({'error': f'Producto con ID {item["id"]} no encontrado'}, status=404)

                cantidad = item['cantidad']
                if cantidad <= 0:
                    return JsonResponse({'error': f'Cantidad inválida para el producto {item["id"]}'}, status=400)
                
                subtotal = producto.precio * cantidad
                total_pedido += subtotal

                PedidoProducto.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=cantidad,
                    subtotal=subtotal
                )

            # Guardar el total en el pedido y actualizarlo
            pedido.total = total_pedido
            pedido.save()

            return JsonResponse({'mensaje': 'Pedido agregado exitosamente'})

        except (json.JSONDecodeError, KeyError) as e:
            print('Error de procesamiento de datos:', e)
            return JsonResponse({'error': f'Error en los datos: {str(e)}'}, status=400)
        except Exception as e:
            print('Error inesperado:', e)  # Log de error detallado
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def login_tablet(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Buscar la mesa por su username y password
        try:
            mesa = Mesa.objects.get(username=username, password=password)
            # Generar un token y almacenarlo en la sesión
            request.session['mesa_token'] = f"{mesa.username}_token"
            # Redirigir al menú si el login es exitoso
            return redirect('home')
        except Mesa.DoesNotExist:
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})

    return render(request, 'login.html')

# Vista personalizada de logout
def logout_view(request):
    logout(request)  # Cerrar sesión
    return redirect('login')  # Redirigir al login después del logout

def carrito(request):
    # Aquí puedes manejar los items del carrito, dependiendo de tu implementación
    return render(request, 'carrito.html')

# Carrito 
def agregar_al_carrito(request, producto_id):
    if request.method == 'GET':
        producto = get_object_or_404(Producto, id=producto_id)
        pedido, _ = Pedido.objects.get_or_create(cliente=request.user, total=0)
        
        # Agregar o actualizar el producto en el carrito
        pedido_producto, created = PedidoProducto.objects.get_or_create(
            pedido=pedido,
            producto=producto,
            defaults={'cantidad': 1, 'subtotal': producto.precio}
        )
        
        if not created:
            pedido_producto.cantidad += 1
            pedido_producto.subtotal = pedido_producto.cantidad * producto.precio
            pedido_producto.save()

        # Recalcular el total del pedido
        pedido.total = sum(item.subtotal for item in pedido.pedidoproducto_set.all())
        pedido.save()

        # Preparar respuesta
        productos_en_carrito = pedido.pedidoproducto_set.all()
        carrito_items = [
            {"nombre": item.producto.nombre, "cantidad": item.cantidad, "subtotal": float(item.subtotal)}
            for item in productos_en_carrito
        ]
        total = float(pedido.total)

        return JsonResponse({"carrito_items": carrito_items, "total": total, "carrito_count": productos_en_carrito.count()})
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
def disminuir_cantidad(request, producto_id):
    pedido = Pedido.objects.get(cliente=request.user)
    pedido_producto = get_object_or_404(PedidoProducto, pedido=pedido, producto_id=producto_id)

    if pedido_producto.cantidad > 1:
        pedido_producto.cantidad -= 1
        pedido_producto.subtotal = pedido_producto.cantidad * pedido_producto.producto.precio
        pedido_producto.save()
    else:
        pedido_producto.delete()  # Si la cantidad es 1, se elimina el producto del carrito

    # Actualizar el total del pedido
    pedido.total = sum(item.subtotal for item in pedido.pedidoproducto_set.all())
    pedido.save()

    return _actualizar_respuesta_carrito(pedido)

def eliminar_del_carrito(request, producto_id):
    pedido = Pedido.objects.get(cliente=request.user)
    pedido_producto = get_object_or_404(PedidoProducto, pedido=pedido, producto_id=producto_id)
    pedido_producto.delete()

    # Actualizar el total del pedido
    pedido.total = sum(item.subtotal for item in pedido.pedidoproducto_set.all())
    pedido.save()

    return _actualizar_respuesta_carrito(pedido)

def _actualizar_respuesta_carrito(pedido):
    productos_en_carrito = pedido.pedidoproducto_set.all()
    carrito_items = [
        {
            "id": item.producto.id,
            "nombre": item.producto.nombre,
            "cantidad": item.cantidad,
            "subtotal": float(item.subtotal),
        }
        for item in productos_en_carrito
    ]
    total = float(pedido.total)

    return JsonResponse({
        "carrito_items": carrito_items,
        "total": total,
        "carrito_count": productos_en_carrito.count()
    })
