from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Tarea

# Create your views here.

# def inicio(request):
#     return HttpResponse("Hola, esta es mi App de Tareas")

def inicio(request):

    return render(request, 'tareasapp/inicio.html')


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
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Obtiene el token si ya existe, o lo crea si es la primera vez
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'message': 'Inicio de sesión exitoso'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'Credenciales inválidas'
            }, status=status.HTTP_401_UNAUTHORIZED)

class TareaAPIView(APIView):

    #Esto es para que solo los usuarios autenticados puedan acceder a esta vista, para ser 
    #mas especifico, para que solo los usuarios que tengan un token valido puedan acceder a esta vista
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # Get lista todas las tareas
    def get(self, request):
        tareas = Tarea.objects.all()
        datos = []

        for tarea in tareas:
            datos.append({
                'id': tarea.id,
                'titulo': tarea.titulo,
                'descripcion': tarea.descripcion,
                'completada': tarea.completada
            })
        return Response(datos, status=status.HTTP_200_OK)    

    def post(self, request):
        titulo = request.data.get('titulo')
        descripcion = request.data.get('descripcion')
        completada = request.data.get('completada', False)

        if not titulo or not descripcion:
            return Response({
                'message': 'El título y la descripción son obligatorios'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        #Crear la tarea y guardarla en la base de datos
        tarea = Tarea.objects.create(
            titulo=titulo,
            descripcion=descripcion,
            completada=completada
        )

        #Devolver la tarea creada como respuesta
        return Response({
            'Mensaje': 'Tarea creada exitosamente',
            'tarea': {
                'id': tarea.id,
                'titulo': tarea.titulo,
                'descripcion': tarea.descripcion,
                'completada': tarea.completada
            }
        }, status=status.HTTP_201_CREATED)
class TareaDetalleAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            tarea = Tarea.objects.get(id=id)
            datos = {
                'id': tarea.id,
                'titulo': tarea.titulo,
                'descripcion': tarea.descripcion,
                'completada': tarea.completada
            }
            return Response(datos, status=status.HTTP_200_OK)
        except Tarea.DoesNotExist:
            return Response({
                'message': 'Tarea no encontrada'
            }, status=status.HTTP_404_NOT_FOUND)
    #Delete: Elimina una tarea por su ID
    def delete(self, request, id):
        try:
            tarea = Tarea.objects.get(id=id)
            tarea.delete()
            return Response({
                'message': 'Tarea eliminada exitosamente'
            }, status=status.HTTP_200_OK)
        except Tarea.DoesNotExist:
            return Response({
                'message': 'Tarea no encontrada'
            }, status=status.HTTP_404_NOT_FOUND)    