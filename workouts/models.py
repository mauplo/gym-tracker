from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.
class Ejercicio(models.Model):
    """Catálogo global de ejercicios (Shoulder Press, Squat, etc.)"""

    """Cada ejercicio corresponde a un grupo muscular principal"""
    GRUPO_MUSCULAR_CHOICES = [
        ('pecho', 'Pecho'),
        ('espalda_alta', 'Espalda Alta'),
        ('espalda_baja', 'Espalda Baja'),
        ('laterales', 'Laterales'),
        ('hombros', 'Hombros'),
        ('biceps', 'Bíceps'),
        ('triceps', 'Tríceps'),
        ('antebrazos', 'Antebrazos'),
        ('cuadriceps', 'Cuádriceps'),
        ('isquiotibiales', 'Isquiotibiales'),
        ('pantorrillas', 'Pantorrillas'),
        ('gluteos', 'Glúteos'),
        ('abdomen', 'Abdomen'),
    ]

    TIPO_EQUIPO_CHOICES = [
        ('mancuerna', 'Mancuerna'),
        ('barra', 'Barra'),
        ('maquina', 'Máquina'),
        ('cable', 'Cable'),
        ('peso_corporal', 'Peso corporal'),
        ('kettlebell', 'Kettlebell'),
        ('banda', 'Banda de resistencia'),
    ]

    nombre = models.CharField(max_length=100) # Nombre del ejercicio, no es unique porque hay ejercicios con el mismo nombre pero diferente equipo
    grupo_muscular = models.CharField(max_length=20, choices=GRUPO_MUSCULAR_CHOICES) # Grupo muscular principal
    tipo_equipo = models.CharField(max_length=20, choices=TIPO_EQUIPO_CHOICES) # Tipo de equipo necesario
    descripcion = models.TextField(blank=True) # Descripción del ejercicio, opcional

    class Meta:
        ordering = ['nombre', 'tipo_equipo']
        unique_together = ('nombre', 'tipo_equipo') # aqui no permitimos que haya ejercicios con el mismo nombre y equipo

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_equipo_display()})"

class Rutina(models.Model):
    """Una rutina que un usuario diseña, ej. 'Upper', 'Lower', 'Full Body'"""

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rutinas') # foreign key del usuario
    nombre = models.CharField(max_length=100) # nombre que le da
    descripcion = models.TextField(blank=True) # descripción opcional
    fecha_creacion = models.DateTimeField(auto_now_add=True) 
    ejercicios = models.ManyToManyField(Ejercicio, through='RutinaEjercicio') # relación muchos a muchos con Ejercicio a través de RutinaEjercicio

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.nombre} ({self.usuario.username})"


class RutinaEjercicio(models.Model):
    """Tabla intermedia: qué ejercicios componen una rutina, en qué orden"""

    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE)
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    orden = models.PositiveIntegerField(default=1)
    series_objetivo = models.PositiveIntegerField(default=3)
    reps_objetivo = models.PositiveIntegerField(default=8)

    class Meta:
        ordering = ['orden']
        unique_together = ('rutina', 'ejercicio')

    def __str__(self):
        return f"{self.ejercicio.nombre} en {self.rutina.nombre}"


class SesionEntrenamiento(models.Model):
    """Un registro de 'hoy entrené' — mide consistencia"""

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sesiones')
    rutina = models.ForeignKey(Rutina, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    notas = models.TextField(blank=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"Sesión de {self.usuario.username} el {self.fecha.strftime('%Y-%m-%d')}"


class RegistroSerie(models.Model):
    """Cada serie realizada dentro de una sesión — mide progreso"""

    UNIDAD_CHOICES = [
        ('kg', 'Kilogramos'),
        ('lb', 'Libras'),
    ]

    sesion = models.ForeignKey(SesionEntrenamiento, on_delete=models.CASCADE, related_name='registros')
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    numero_serie = models.PositiveIntegerField()
    peso = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)]) # no hay pesos negativos
    repeticiones = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unidad = models.CharField(max_length=2, choices=UNIDAD_CHOICES, default='kg')

    class Meta:
        ordering = ['sesion', 'ejercicio', 'numero_serie']

    def __str__(self):
        return f"{self.ejercicio.nombre}: {self.peso}{self.unidad} x {self.repeticiones}"