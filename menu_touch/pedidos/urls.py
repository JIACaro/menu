from django.urls import path
from . import views  # Importamos las vistas de la app

urlpatterns = [
    path('', views.home, name='home'),  
    path('login/', views.login_tablet, name='login'),  # Ruta para la página de login
    path('menu/', views.menu, name='menu'),  # Ruta para el menú
    path('logout/', views.logout_view, name='logout'),  # Ruta para el logout
]
