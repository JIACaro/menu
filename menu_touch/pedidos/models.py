from django.db import models
from django.conf import settings


# Modelo Producto
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)  # Descripción del producto
    stock = models.PositiveIntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)  # Campo para la imagen del producto

    def __str__(self):
        return self.nombre
    
# Modelo Pedido
class Pedido(models.Model):
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    productos = models.ManyToManyField(Producto, through='PedidoProducto')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Pedido #{self.id} - Cliente: {self.cliente.username}"

# Modelo intermedio para manejar la cantidad de productos en un pedido
class PedidoProducto(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

# Modelo PerfilUsuario (si no estás usando un modelo de usuario personalizado)
class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    es_cliente = models.BooleanField(default=True)
    es_empleado = models.BooleanField(default=False)
    es_gerente = models.BooleanField(default=False)

    def __str__(self):
        return self.usuario.username

class Mesa(models.Model):
    username = models.CharField(max_length=50, unique=True)  # Nombre de usuario, único por mesa
    password = models.CharField(max_length=50)  # Contraseña

    def __str__(self):
        return f"{self.username}"
