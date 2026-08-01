from django.shortcuts import render

# Create your views here.
# ViewSets: la lógica que conecta URLs con lógica de negocio (listar, crear, editar, borrar)
# Permissions: deciden quién puede ver/editar qué (cada usuario solo sus propios datos)

from rest_framework import viewsets, permissions
from .models import Ejercicio, Rutina, SesionEntrenamiento, RegistroSerie
from .serializers import (
    EjercicioSerializer, RutinaSerializer,
    SesionEntrenamientoSerializer, RegistroSerieSerializer
)



class EsPropietarioOSoloLectura(permissions.BasePermission): # permiso personalizado a nivel del objeto, podemos cambiar si es público/privado
    """
    Cualquier usuario autenticado puede leer.
    Solo el dueño del objeto puede editarlo o borrarlo.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        return obj.usuario == request.user


class EjercicioViewSet(viewsets.ModelViewSet):
    """Catálogo global — todos los usuarios autenticados pueden leerlo.
    Por ahora, solo el staff puede crear/editar (es un catálogo compartido)."""
    queryset = Ejercicio.objects.all()
    serializer_class = EjercicioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]


class RutinaViewSet(viewsets.ModelViewSet):
    serializer_class = RutinaSerializer
    permission_classes = [permissions.IsAuthenticated, EsPropietarioOSoloLectura]

    def get_queryset(self):
        # cada usuario solo ve SUS PROPIAS rutinas, no las de todos
        return Rutina.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        # el dueño se asigna del usuario autenticado, nunca del input del cliente
        serializer.save(usuario=self.request.user)


class SesionEntrenamientoViewSet(viewsets.ModelViewSet):
    serializer_class = SesionEntrenamientoSerializer
    permission_classes = [permissions.IsAuthenticated, EsPropietarioOSoloLectura]

    def get_queryset(self): # filtrado por usuario, autorización a nivel objeto
        return SesionEntrenamiento.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer): # asigna al dueño
        serializer.save(usuario=self.request.user)


class RegistroSerieViewSet(viewsets.ModelViewSet):
    serializer_class = RegistroSerieSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # solo registros de sesiones que pertenecen al usuario autenticado
        return RegistroSerie.objects.filter(sesion__usuario=self.request.user)
