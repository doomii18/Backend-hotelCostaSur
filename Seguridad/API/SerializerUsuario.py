from rest_framework import serializers
from Seguridad.models import Usuario


class SerializerUsuario(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id_usuario', 'usuario', 'correo', 'contrasena', 'rol', 'fecha_registro']
        extra_kwargs = {
            'contrasena': {'write_only': True}
        }

    def create(self, validated_data):
        # Create user and hash the password correctly
        password = validated_data.pop('contrasena', '')
        usuario = Usuario(**validated_data)
        usuario.set_password(password)
        usuario.save()
        return usuario
