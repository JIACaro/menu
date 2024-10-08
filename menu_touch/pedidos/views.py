from django.shortcuts import render, redirect
from .models import Producto, Mesa
from django.contrib.auth import logout
from django.shortcuts import redirect

def home(request):
    # Obtenemos el token de la sesión y extraemos el nombre de la mesa
    mesa_token = request.session.get('mesa_token', 'Mesa Desconocida')
    mesa_nombre = mesa_token.split('_')[0]  # Extraer el nombre de la mesa del token (por ejemplo: "mesa1")
    
    return render(request, 'home.html', {'mesa_nombre': mesa_nombre})


def menu(request):
    productos = Producto.objects.all()  # Obtener productos desde el modelo Producto
    return render(request, 'menu.html', {'productos': productos})

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
