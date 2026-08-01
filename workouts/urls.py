from django.urls import path
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from . import views
from .views import (
    EjercicioViewSet, RutinaViewSet,
    SesionEntrenamientoViewSet, RegistroSerieViewSet
)

# --- Rutas de la API ---
router = DefaultRouter() # generamos los URLs REST para cada ViewSet automáticamente (GET/POST/PUT/DELETE)
router.register(r'ejercicios', EjercicioViewSet, basename='ejercicio')
router.register(r'rutinas', RutinaViewSet, basename='rutina')
router.register(r'sesiones', SesionEntrenamientoViewSet, basename='sesion')
router.register(r'registros', RegistroSerieViewSet, basename='registro')

api_urlpatterns = router.urls

# --- Rutas del frontend ---
frontend_urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('rutinas/<int:rutina_id>/', views.rutina_detalle_view, name='rutina_detalle'),
]