from rest_framework import serializers
from .models import Contacto

class ContactoSerializer(serializers.ModelSerializer):
    
    usuario_username = serializers.ReadOnlyField(source='usuario.username')
    edad = serializers.ReadOnlyField()
    
    class Meta:
        model = Contacto
        fields = [
            'id',
            'usuario',
            'usuario_username',
            'nombre',
            'telefono',
            'email',
            'direccion',
            'fecha_nacimiento',
            'edad',
            'notas',
            'foto',
            'favorito',
            'fecha_creacion',
            'fecha_actualizacion'
        ]
        read_only_fields = ['usuario', 'fecha_creacion', 'fecha_actualizacion']
    
    def validate_telefono(self, value):
        if value and len(value) < 10:
            raise serializers.ValidationError("El teléfono debe tener al menos 10 dígitos")
        return value