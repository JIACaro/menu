from django.urls import path
from . import views

urlpatterns = [
    path('ordenes/', views.vista_cocina, name='vista_cocina'),
    path('cambiar-estado-pedido/<int:order_id>/', views.cambiar_estado_pedido, name='cambiar_estado_pedido'),

]
