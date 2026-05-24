from rest_framework import serializers
from Seguridad.Usuarios.models import Usuario


class SerializerUsuario(serializers.ModelSerializer):
    # Alias para que el frontend reciba nombres consistentes
    id = serializers.IntegerField(source='id_usuario', read_only=True)
    nombre = serializers.CharField(source='usuario')
    email = serializers.CharField(source='correo')
    fechaRegistro = serializers.DateTimeField(source='fecha_registro', read_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'id_usuario', 'nombre', 'email', 'rol', 'fechaRegistro', 'Estado']
        extra_kwargs = {
            'contrasena': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('contrasena', '')
        usuario = Usuario(**validated_data)
        usuario.set_password(password)
        usuario.save()
        return usuario
