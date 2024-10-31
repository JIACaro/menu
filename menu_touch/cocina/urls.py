from django.urls import path
from . import views

urlpatterns = [
    path('ordenes/', views.vista_cocina, name='vista_cocina'),
]
