from django import forms
from .models import Contacto, Producto
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .validators import MaxSizerFileValidator
from django.forms import ValidationError


class ContactoForm(forms.ModelForm):

    # Forma de agregar bootstrap
    # nombre = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Contacto
        # fields = ['nombre', 'correo', 'tipo_consulta', 'mensaje', 'avisos']
        fields = '__all__'


class ProductoForms(forms.ModelForm):

    # Validar caracteres min, max
    nombre = forms.CharField(min_length=3, max_length=50)
    # Validar imagen no requerida
    imagen = forms.ImageField(required= False, validators=[MaxSizerFileValidator(max_file_size=2)])
    # Valida maximo y minimo
    precio = forms.IntegerField(min_value=1, max_value=1500000)

    # Valida que no se repitan el nombre
    def clean_nombre(self):
        # Comprueba de la DB
        nombre = self.cleaned_data['nombre']
        existe = Producto.objects.filter(nombre__iexact = nombre).exists()

        if(existe):
            raise ValidationError('Este nombre ya existe')
        
        return nombre

    class Meta:
        model = Producto
        fields = '__all__'

        widgets = {
            'fecha_fabricacion': forms.SelectDateWidget()
        }

class CustomUserCreationForm(UserCreationForm):
    model = User

    class Meta:
        model  = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']