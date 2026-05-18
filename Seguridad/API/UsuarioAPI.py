from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from Seguridad.models import Usuario
from Seguridad.API.SerializerUsuario import SerializerUsuario


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all().order_by('id_usuario')
    serializer_class = SerializerUsuario

    @action(detail=False, methods=['post'], url_path='register')
    def register_user(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': f'¡Huésped {user.usuario} registrado con éxito! 🎉'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='login')
    def login_user(self, request):
        usuario_input = request.data.get('usuario')
        contrasena_input = request.data.get('contrasena')

        if not usuario_input or not contrasena_input:
            return Response({
                'message': 'Por favor ingresa usuario y contraseña.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Check by username or email
            user = Usuario.objects.filter(usuario=usuario_input).first() or \
                   Usuario.objects.filter(correo=usuario_input).first()

            if user and user.check_password(contrasena_input):
                # Issue JWT Access Token with custom claims matching frontend expectation
                token = AccessToken()
                token['id'] = user.id_usuario
                token['rol'] = user.rol
                token['usuario'] = user.usuario

                return Response({
                    'message': 'Inicio de sesión exitoso.',
                    'token': str(token),
                    'user': {
                        'id': user.id_usuario,
                        'usuario': user.usuario,
                        'correo': user.correo,
                        'rol': user.rol
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'message': 'Usuario o contraseña incorrectos.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                'message': f'Error en el servidor: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
