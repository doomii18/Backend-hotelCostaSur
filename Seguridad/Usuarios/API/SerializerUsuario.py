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

    def validate(self, attrs):
        usuario_val = attrs.get('usuario')
        correo_val = attrs.get('correo')

        if usuario_val:
            qs = Usuario.objects.filter(usuario=usuario_val)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError({
                    'nombre': 'El nombre de usuario ya está registrado.'
                })

        if correo_val:
            qs = Usuario.objects.filter(correo=correo_val)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError({
                    'email': 'El correo electrónico ya está registrado.'
                })

        return attrs

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

