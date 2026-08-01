from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import SesionEntrenamiento, RegistroSerie
from django.forms import modelformset_factory


class SignUpForm(UserCreationForm): # clase base para validar usuarios y contraseñas
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Registrar una sesión de entrenamiento con sus series
class SesionEntrenamientoForm(forms.ModelForm):
    class Meta:
        model = SesionEntrenamiento
        fields = ['rutina', 'notas']
        widgets = {
            'notas': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, usuario=None, **kwargs): # seguridad: el usuario autenticado se pasa desde la vista, no desde el formulario
        super().__init__(*args, **kwargs)
        # solo mostrar rutinas del usuario actual en el dropdown, no las de todos
        if usuario:
            self.fields['rutina'].queryset = self.fields['rutina'].queryset.filter(usuario=usuario)
        self.fields['rutina'].required = False


class RegistroSerieForm(forms.ModelForm):
    class Meta:
        model = RegistroSerie
        fields = ['ejercicio', 'numero_serie', 'peso', 'repeticiones', 'unidad']


RegistroSerieFormSet = modelformset_factory(
    RegistroSerie,
    form=RegistroSerieForm,
    extra=4,       # 4 filas vacías por defecto (ajustable por el usuario)
    can_delete=True,
)