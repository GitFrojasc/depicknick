from django import forms
from .models import Suscripcion


class SuscripcionForm(forms.ModelForm):
    class Meta:
        model = Suscripcion
        fields = ['nombre_cliente', 'email', 'telefono', 'ciudad', 'direccion', 'frecuencia']
        labels = {
            'nombre_cliente': 'Tu nombre',
            'email': 'Correo electrónico',
            'telefono': 'WhatsApp / Teléfono',
            'ciudad': 'Ciudad',
            'direccion': 'Dirección de entrega',
            'frecuencia': '¿Con qué frecuencia quieres tu canasto?',
        }
        widgets = {
            'nombre_cliente': forms.TextInput(attrs={'placeholder': 'Ej: María García'}),
            'email': forms.EmailInput(attrs={'placeholder': 'tu@correo.com'}),
            'telefono': forms.TextInput(attrs={'placeholder': '+57 300 123 4567'}),
            'ciudad': forms.TextInput(attrs={'placeholder': 'Pereira, Manizales, Armenia...'}),
            'direccion': forms.Textarea(attrs={'placeholder': 'Calle, barrio, referencias...', 'rows': 3}),
            'frecuencia': forms.Select(),
        }
