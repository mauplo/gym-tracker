from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Max
from .forms import SignUpForm, SesionEntrenamientoForm, RegistroSerieFormSet
import json
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

# Agregamos vistas para el front
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Cuenta creada exitosamente!')
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def dashboard_view(request):
    rutinas = Rutina.objects.filter(usuario=request.user)
    sesiones_recientes = SesionEntrenamiento.objects.filter(usuario=request.user)[:5]
    return render(request, 'workouts/dashboard.html', {
        'rutinas': rutinas,
        'sesiones_recientes': sesiones_recientes,
    })


@login_required
def rutina_detalle_view(request, rutina_id):
    # get_object_or_404 + filtro por usuario: si la rutina no es tuya, da 404 (no 403)
    # esto evita revelar si el objeto existe pero pertenece a otro usuario
    rutina = get_object_or_404(Rutina, id=rutina_id, usuario=request.user)
    return render(request, 'workouts/rutina_detalle.html', {'rutina': rutina})

@login_required
def sesion_crear_view(request):
    if request.method == 'POST':
        sesion_form = SesionEntrenamientoForm(request.POST, usuario=request.user)
        formset = RegistroSerieFormSet(request.POST, queryset=RegistroSerie.objects.none())

        if sesion_form.is_valid() and formset.is_valid():
            sesion = sesion_form.save(commit=False)
            sesion.usuario = request.user  # el dueño se asigna aquí, no viene del form
            sesion.save()

            registros_guardados = 0
            for form in formset:
                # ignora filas vacías que el usuario no llenó
                if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                    if form.cleaned_data.get('ejercicio'):
                        registro = form.save(commit=False)
                        registro.sesion = sesion
                        registro.save()
                        registros_guardados += 1

            messages.success(request, f'Sesión guardada con {registros_guardados} series registradas.')
            return redirect('dashboard')
    else:
        sesion_form = SesionEntrenamientoForm(usuario=request.user)
        formset = RegistroSerieFormSet(queryset=RegistroSerie.objects.none())

    return render(request, 'workouts/sesion_form.html', {
        'sesion_form': sesion_form,
        'formset': formset,
    })
# Vista para gráfica de progreso de un ejercicio específico
@login_required
def progreso_ejercicio_view(request, ejercicio_id):
    ejercicio = get_object_or_404(Ejercicio, id=ejercicio_id)

    registros = (
        RegistroSerie.objects
        .filter(sesion__usuario=request.user, ejercicio=ejercicio)
        .values('sesion__fecha')
        .annotate(peso_maximo=Max('peso'))
        .order_by('sesion__fecha')
    )

    fechas = [r['sesion__fecha'].strftime('%Y-%m-%d') for r in registros]
    pesos = [float(r['peso_maximo']) for r in registros]

    return render(request, 'workouts/progreso.html', {
        'ejercicio': ejercicio,
        'fechas_json': json.dumps(fechas),
        'pesos_json': json.dumps(pesos),
        'tiene_datos': len(fechas) > 0,
    })