from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, EmailValidator
from django.utils import timezone
import re

class Contacto(models.Model):
    
    telefono_validator = RegexValidator(
        regex=r'^\+?[\d\s-]{10,20}$',
        message="El teléfono debe tener entre 10 y 20 caracteres y puede incluir +, espacios o guiones."
    )
    
    usuario = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='contactos',
        verbose_name='Usuario'
    )
    
    nombre = models.CharField(
        max_length=100,
        verbose_name='Nombre completo',
        help_text='Nombre completo del contacto'
    )
    
    telefono = models.CharField(
        max_length=20,
        validators=[telefono_validator],
        verbose_name='Teléfono',
        blank=True,
        null=True
    )
    
    email = models.EmailField(
        max_length=100,
        validators=[EmailValidator()],
        verbose_name='Correo electrónico',
        blank=True,
        null=True
    )
    
    direccion = models.TextField(
        max_length=200,
        verbose_name='Dirección',
        blank=True,
        null=True,
        help_text='Dirección completa del contacto'
    )
    
    foto = models.ImageField(
        upload_to='contactos_fotos/',
        verbose_name='Foto',
        blank=True,
        null=True
    )
    
    fecha_nacimiento = models.DateField(
        verbose_name='Fecha de nacimiento',
        blank=True,
        null=True
    )
    
    notas = models.TextField(
        max_length=500,
        verbose_name='Notas adicionales',
        blank=True,
        null=True
    )
    
    fecha_creacion = models.DateTimeField(
        default=timezone.now,
        verbose_name='Fecha de creación'
    )
    
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Última actualización'
    )
    
    favorito = models.BooleanField(
        default=False,
        verbose_name='Contacto favorito'
    )
    
    class Meta:
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'
        ordering = ['-favorito', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} - {self.usuario.username}"
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('detalle_contacto', args=[str(self.id)])
    
    def edad(self):
        if self.fecha_nacimiento:
            from datetime import date
            today = date.today()
            return today.year - self.fecha_nacimiento.year - (
                (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
            )
        return None
    
    def telefono_limpio(self):
        if self.telefono:
            return re.sub(r'[\s-]', '', self.telefono)
        return ''