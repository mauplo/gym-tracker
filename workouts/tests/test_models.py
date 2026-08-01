import pytest
from django.db import IntegrityError
from workouts.factories import EjercicioFactory, RutinaFactory, UserFactory
from workouts.models import Ejercicio

pytestmark = pytest.mark.django_db  # habilita acceso a la BD en estos tests


class TestEjercicio:

    def test_str_representation(self):
        ejercicio = EjercicioFactory(nombre='Shoulder Press', tipo_equipo='mancuerna')
        assert str(ejercicio) == 'Shoulder Press (Mancuerna)'

    def test_mismo_nombre_distinto_equipo_es_valido(self):
        """Debe poder existir 'Shoulder Press' en mancuerna Y en máquina"""
        EjercicioFactory(nombre='Shoulder Press', tipo_equipo='mancuerna')
        EjercicioFactory(nombre='Shoulder Press', tipo_equipo='maquina')
        assert Ejercicio.objects.filter(nombre='Shoulder Press').count() == 2

    def test_mismo_nombre_y_equipo_no_es_valido(self):
        """No debe permitir duplicados exactos (nombre + equipo)"""
        EjercicioFactory(nombre='Squat', tipo_equipo='barra')
        with pytest.raises(IntegrityError):
            EjercicioFactory(nombre='Squat', tipo_equipo='barra')


class TestRutina:

    def test_rutina_pertenece_a_usuario(self):
        usuario = UserFactory()
        rutina = RutinaFactory(usuario=usuario)
        assert rutina.usuario == usuario
        assert rutina in usuario.rutinas.all()