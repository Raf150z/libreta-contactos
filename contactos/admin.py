from django.contrib import admin
from .models import Contacto

@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    
    list_display = ['nombre', 'usuario', 'telefono', 'email', 'favorito', 'fecha_creacion']
    list_filter = ['usuario', 'favorito', 'fecha_creacion']
    search_fields = ['nombre', 'telefono', 'email', 'direccion']
    list_editable = ['favorito']
    list_per_page = 20
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('usuario', 'nombre', 'foto')
        }),
        ('Información de Contacto', {
            'fields': ('telefono', 'email', 'direccion')
        }),
        ('Información Adicional', {
            'fields': ('fecha_nacimiento', 'notas', 'favorito')
        }),
        ('Metadata', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']