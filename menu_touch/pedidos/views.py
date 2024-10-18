from django.shortcuts import render, redirect
from .models import Producto, Mesa
from django.contrib.auth import logout
from django.shortcuts import redirect

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

def menu(request):
    mesa_token = request.session.get('mesa_token', None)
    mesa_nombre = mesa_token.split('_')[0] if mesa_token else "Desconocida"
    
    # Supongamos que obtienes los productos de tu modelo
    productos = Producto.objects.all()
    
    return render(request, 'menu.html', {'productos': productos, 'mesa_nombre': mesa_nombre})

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
