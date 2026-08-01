from rest_framework.routers import DefaultRouter
from .views import (
    EjercicioViewSet, RutinaViewSet,
    SesionEntrenamientoViewSet, RegistroSerieViewSet
)

router = DefaultRouter()
router.register(r'ejercicios', EjercicioViewSet, basename='ejercicio')
router.register(r'rutinas', RutinaViewSet, basename='rutina')
router.register(r'sesiones', SesionEntrenamientoViewSet, basename='sesion')
router.register(r'registros', RegistroSerieViewSet, basename='registro')

urlpatterns = router.urls