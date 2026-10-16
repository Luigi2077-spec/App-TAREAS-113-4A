from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Tarea
# Create your views here.

# def inicio(request):
#     return HttpResponse("Hola, esta es mi App de Tareas")

def inicio(request):
    tareas = Tarea.objects.all()

    return render(request, 'tareasapp/inicio.html', {
        'tareas': tareas
    }) 


def crear_tarea(request):
    if request.method == 'POST':
        titulo = request.POST['titulo']
        descripcion = request.POST['descripcion']
        completada = 'completa'in request.POST

        Tarea.objects.create(
            titulo = titulo,
            descripcion = descripcion,
            completada = completada
        )
        return redirect('inicio')
    return render (request, 'tareasapp/crear.html')


def detalle_tarea(request, id):
    tarea = Tarea.objects.get(id=id)

    return render(request, 'tareasapp/detalle.html', {
        'tarea': tarea
    })


def editar_tarea(request, id):
    tarea = Tarea.objects.get(id=id)

    if request.method == 'POST':
        tarea.titulo = request.POST['titulo']
        tarea.descripcion = request.POST['descripcion']
        tarea.completada = 'completada' in request.POST

        tarea.save()
        return redirect('inicio')
    
    return render(request, 'tareasapp/editar.html', {
        'tarea': tarea
    })

def eliminar_tarea(request, id):
    tarea = Tarea.objects.get(id=id)

    if request.method == 'POST':
        tarea.delete()

        return redirect('inicio')
    
    return render(request, 'tareasapp/eliminar.html', {
        'tarea': tarea
    })

def login_pagina(request):
    return render(request, 'tareasapp/login.html')

class LoginAPIView(APIView):
    permission_classes=[AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        #Validar que se proporcionen el nombre de usuario y la contraseña
        user = authenticate(request, username=username, password=password)

        if user is not None:
            return Response({'message': 'Inicio de sesión exitoso'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)