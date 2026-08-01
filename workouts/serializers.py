from rest_framework import serializers
from .models import Ejercicio, Rutina, RutinaEjercicio, SesionEntrenamiento, RegistroSerie

# Serializers define the API representation. 
# i.e. convierten objetos Python (modelos) a JSON y viceversa, y validan datos entrantes
class EjercicioSerializer(serializers.ModelSerializer): # ModelSerializer checa las reglas de nuestra DB
    class Meta:
        model = Ejercicio
        fields = ['id', 'nombre', 'grupo_muscular', 'tipo_equipo', 'descripcion']


class RutinaEjercicioSerializer(serializers.ModelSerializer):
    ejercicio_nombre = serializers.CharField(source='ejercicio.nombre', read_only=True)

    class Meta:
        model = RutinaEjercicio
        fields = ['id', 'ejercicio', 'ejercicio_nombre', 'orden', 'series_objetivo', 'reps_objetivo']


class RutinaSerializer(serializers.ModelSerializer):
    # nested: al leer una rutina, incluye el detalle de sus ejercicios
    rutina_ejercicios = RutinaEjercicioSerializer(source='rutinaejercicio_set', many=True, read_only=True)

    class Meta:
        model = Rutina
        fields = ['id', 'nombre', 'descripcion', 'fecha_creacion', 'usuario', 'rutina_ejercicios']
        read_only_fields = ['usuario']  # se asigna automáticamente, no lo manda el cliente


class RegistroSerieSerializer(serializers.ModelSerializer):
    ejercicio_nombre = serializers.CharField(source='ejercicio.nombre', read_only=True) # source: para mostrar el nombre del ejercicio en vez de solo el ID

    class Meta:
        model = RegistroSerie
        fields = ['id', 'sesion', 'ejercicio', 'ejercicio_nombre', 'numero_serie', 'peso', 'repeticiones', 'unidad']


class SesionEntrenamientoSerializer(serializers.ModelSerializer):
    registros = RegistroSerieSerializer(many=True, read_only=True) # te trae todos los registros de series asociados a esta sesión

    class Meta:
        model = SesionEntrenamiento
        fields = ['id', 'usuario', 'rutina', 'fecha', 'notas', 'registros']
        read_only_fields = ['usuario'] # el cliente no debe mandar este dato