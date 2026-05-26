from rest_framework import serializers
from Seguridad.Usuarios.models import Usuario


class SerializerUsuario(serializers.ModelSerializer):
    # Alias para que el frontend reciba nombres consistentes
    id = serializers.IntegerField(source='id_usuario', read_only=True)
    nombre = serializers.CharField(source='usuario')
    email = serializers.CharField(source='correo')
    password = serializers.CharField(write_only=True, required=False)
    fechaRegistro = serializers.DateTimeField(source='fecha_registro', read_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'id_usuario', 'nombre', 'email', 'password', 'rol', 'fechaRegistro', 'Estado']

    def create(self, validated_data):
        password = validated_data.pop('password', '')
        usuario = Usuario(**validated_data)
        usuario.set_password(password)
        usuario.save()
        return usuario

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
