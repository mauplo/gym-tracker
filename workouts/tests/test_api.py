import pytest
from rest_framework.test import APIClient
from rest_framework import status
from workouts.factories import UserFactory, RutinaFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def usuario_autenticado(api_client):
    usuario = UserFactory(password='testpass123')
    api_client.force_authenticate(user=usuario)
    return usuario


class TestRutinaAPI:

    def test_usuario_no_autenticado_no_puede_acceder(self, api_client):
        response = api_client.get('/api/rutinas/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_usuario_autenticado_puede_listar_sus_rutinas(self, api_client, usuario_autenticado):
        RutinaFactory(usuario=usuario_autenticado, nombre='Mi rutina')
        response = api_client.get('/api/rutinas/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['nombre'] == 'Mi rutina'

    def test_usuario_no_ve_rutinas_de_otros(self, api_client, usuario_autenticado):
        """Test de seguridad crítico: aislamiento de datos entre usuarios"""
        otro_usuario = UserFactory()
        RutinaFactory(usuario=otro_usuario, nombre='Rutina ajena')

        response = api_client.get('/api/rutinas/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0  # no debe ver la rutina del otro usuario

    def test_no_se_puede_asignar_usuario_manualmente(self, api_client, usuario_autenticado):
        """Test de seguridad crítico: el campo 'usuario' no debe venir del cliente"""
        otro_usuario = UserFactory()
        response = api_client.post('/api/rutinas/', {
            'nombre': 'Rutina sospechosa',
            'usuario': otro_usuario.id,  # intento de asignarla a otro usuario
        })
        assert response.status_code == status.HTTP_201_CREATED
        # la rutina debe quedar asociada a quien la creó, NO al usuario enviado en el body
        assert response.data['usuario'] == usuario_autenticado.id