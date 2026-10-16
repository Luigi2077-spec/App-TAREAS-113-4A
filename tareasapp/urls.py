from django.urls import path
from . import views


urlpatterns = [
    #Pagina principal de login
    path('', views.login_pagina, name= 'login_pagina'),
    #Lista de tareas
    path('inicio/', views.inicio, name='inicio'),
    path('crear/', views.crear_tarea, name='crear_tarea'),
    path('detalle/<int:id>', views.detalle_tarea, name='detalle_tarea'),
    path('editar/<int:id>', views.editar_tarea, name='editar_tarea'),
    path('eliminar/<int:id>', views.eliminar_tarea, name='eliminar_tarea'),

    #API REST para autenticacion de usuarios
    path('api/login/', views.LoginAPIView.as_view(), name='api_login'),
]