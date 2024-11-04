from django.urls import path
from . import views  # Importamos las vistas de la app

urlpatterns = [
    path('', views.home, name='home'),  
    path('login/', views.login_tablet, name='login'),  # Ruta para la página de login
    path('categorias/', views.categorias, name='categorias'),
    path('menu/', views.menu, name='menu'),  # Ruta para el menú
    path('logout/', views.logout_view, name='logout'),  # Ruta para el logout
    path('agregar-al-carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('disminuir-cantidad/<int:producto_id>/', views.disminuir_cantidad, name='disminuir_cantidad'),
    path('eliminar-del-carrito/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('agregar-pedido/', views.agregar_pedido, name='agregar_pedido'),
]
