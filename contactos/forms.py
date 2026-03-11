import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Contacto

class RegistroUsuarioForm(UserCreationForm):
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com'
        })
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu nombre'
        })
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu apellido'
        })
    )
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de usuario'
        })
    )
    
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        }),
        help_text="""
            <ul class="text-muted small">
                <li>Mínimo 8 caracteres</li>
                <li>No puede ser similar a tu nombre de usuario</li>
                <li>No puede ser una contraseña común</li>
            </ul>
        """
    )
    
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Este nombre de usuario ya está en uso.')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise ValidationError('Ingresa un email válido (ejemplo: usuario@dominio.com)')
        
        if User.objects.filter(email=email).exists():
            raise ValidationError('Este email ya está registrado. ¿Olvidaste tu contraseña?')
        
        return email
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        username = self.cleaned_data.get('username')
        
        if len(password) < 8:
            raise ValidationError('La contraseña debe tener al menos 8 caracteres')
        
        if username and username.lower() in password.lower():
            raise ValidationError('La contraseña no puede contener tu nombre de usuario')
        
        if not any(c.isalpha() for c in password):
            raise ValidationError('La contraseña debe contener al menos una letra')
        
        if not any(c.isdigit() for c in password):
            raise ValidationError('La contraseña debe contener al menos un número')
        
        common_passwords = ['12345678', 'password', 'qwerty123', 'admin123', '123456789']
        if password in common_passwords:
            raise ValidationError('Esta contraseña es muy común. Elige una más segura')
        
        return password


class ContactoForm(forms.ModelForm):
    
    class Meta:
        model = Contacto
        fields = ['nombre', 'telefono', 'email', 'direccion', 'fecha_nacimiento', 'notas', 'favorito', 'foto']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+52 555 555 5555'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Dirección completa'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'notas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Notas adicionales...'
            }),
            'favorito': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'foto': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }
    
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        
        if telefono:
            telefono_limpio = telefono.replace(' ', '').replace('-', '').replace('+', '')
            
            if not telefono_limpio.isdigit():
                raise ValidationError('El teléfono solo debe contener números, espacios, guiones y +')
            
            if len(telefono_limpio) < 8:
                raise ValidationError('El teléfono debe tener al menos 8 dígitos')
            if len(telefono_limpio) > 15:
                raise ValidationError('El teléfono no puede tener más de 15 dígitos')
            
            if telefono.startswith('+'):
                return telefono
            elif telefono_limpio.startswith('52') and len(telefono_limpio) >= 10:
                return f"+52 {telefono_limpio[2:5]} {telefono_limpio[5:8]} {telefono_limpio[8:]}"
        
        return telefono
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower().strip()
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                raise ValidationError('Ingresa un email válido')
        return email