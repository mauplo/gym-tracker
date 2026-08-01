import factory
from django.contrib.auth.models import User
from .models import Ejercicio, Rutina, SesionEntrenamiento, RegistroSerie

#Con factories, UserFactory() te da un usuario válido con un solo llamado, 
# y se puede sobreescribir solo lo que importa para ese test específico 
# (ej. UserFactory(username='mau')).

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True # no llamar a save() automáticamente, lo hacemos en password

    username = factory.Sequence(lambda n: f'usuario{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        self.set_password(extracted or 'testpass123')
        if create:
            self.save()


class EjercicioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ejercicio

    nombre = factory.Sequence(lambda n: f'Ejercicio {n}')
    grupo_muscular = 'pecho'
    tipo_equipo = 'mancuerna'


class RutinaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Rutina

    usuario = factory.SubFactory(UserFactory)
    nombre = factory.Sequence(lambda n: f'Rutina {n}')


class SesionEntrenamientoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SesionEntrenamiento

    usuario = factory.SubFactory(UserFactory)