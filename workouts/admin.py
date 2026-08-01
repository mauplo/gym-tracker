from django.contrib import admin
from .models import Ejercicio, Rutina, RutinaEjercicio, SesionEntrenamiento, RegistroSerie

# Register your models here.
admin.site.register(Ejercicio)
admin.site.register(Rutina)
admin.site.register(RutinaEjercicio)
admin.site.register(SesionEntrenamiento)
admin.site.register(RegistroSerie)