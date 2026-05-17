from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Suscripcion, Pedido, PerfilCliente


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


class RegistroForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=100, label='Nombre',
        widget=forms.TextInput(attrs={'placeholder': 'Ej: María'}),
    )
    last_name = forms.CharField(
        max_length=100, label='Apellidos',
        widget=forms.TextInput(attrs={'placeholder': 'Ej: García López'}),
    )
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'placeholder': 'tu@correo.com'}),
    )
    telefono = forms.CharField(
        max_length=20, label='WhatsApp / Teléfono',
        widget=forms.TextInput(attrs={'placeholder': '+57 300 123 4567'}),
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'telefono')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Ej: maria.garcia'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            PerfilCliente.objects.create(
                usuario=user,
                telefono=self.cleaned_data['telefono'],
            )
        return user


class CheckoutForm(forms.Form):
    nombre_cliente = forms.CharField(
        max_length=200, label='Nombre completo',
        widget=forms.TextInput(attrs={'placeholder': 'Ej: María García'}),
    )
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'placeholder': 'tu@correo.com'}),
    )
    telefono = forms.CharField(
        max_length=20, label='WhatsApp / Teléfono',
        widget=forms.TextInput(attrs={'placeholder': '+57 300 123 4567'}),
    )
    ciudad = forms.CharField(
        max_length=100, label='Ciudad',
        widget=forms.TextInput(attrs={'placeholder': 'Pereira, Manizales, Armenia...'}),
    )
    direccion = forms.CharField(
        label='Dirección de entrega',
        widget=forms.Textarea(attrs={'placeholder': 'Calle, barrio, referencias...', 'rows': 3}),
    )
    notas = forms.CharField(
        required=False, label='Notas adicionales (opcional)',
        widget=forms.Textarea(attrs={'placeholder': 'Instrucciones especiales para la entrega...', 'rows': 2}),
    )
