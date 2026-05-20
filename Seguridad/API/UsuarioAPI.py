from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from Seguridad.models import Usuario
from Seguridad.API.SerializerUsuario import SerializerUsuario


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all().order_by('id_usuario')
    serializer_class = SerializerUsuario

    # ── LISTAR (solo activos - Estado=True) ────────────────────
    @action(detail=False, methods=['get'], url_path='listar')
    def listar(self, request):
        usuarios = Usuario.objects.filter(Estado=True).order_by('id_usuario')
        serializer = self.get_serializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # ── LISTAR TODOS (admin - activos e inactivos) ─────────────
    @action(detail=False, methods=['get'], url_path='listar-todos')
    def listar_todos(self, request):
        usuarios = Usuario.objects.all().order_by('id_usuario')
        serializer = self.get_serializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # ── REGISTRO ───────────────────────────────────────────────
    @action(detail=False, methods=['post'], url_path='registro')
    def register_user(self, request):
        mapped_data = {
            'usuario': request.data.get('nombre'),
            'correo': request.data.get('email'),
            'contrasena': request.data.get('password'),
            'rol': request.data.get('rol', 'user')
        }
        serializer = self.get_serializer(data=mapped_data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': f'Huesped {user.usuario} registrado con exito!'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ── LOGIN ──────────────────────────────────────────────────
    @action(detail=False, methods=['post'], url_path='login')
    def login_user(self, request):
        usuario_input = request.data.get('nombre')
        contrasena_input = request.data.get('password')

        if not usuario_input or not contrasena_input:
            return Response({
                'message': 'Por favor ingresa usuario y contrasena.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Buscar por usuario o correo, solo activos
            user = Usuario.objects.filter(usuario=usuario_input, Estado=True).first() or \
                   Usuario.objects.filter(correo=usuario_input, Estado=True).first()

            if user and user.check_password(contrasena_input):
                token = AccessToken()
                token['id'] = user.id_usuario
                token['rol'] = user.rol
                token['usuario'] = user.usuario

                return Response({
                    'message': 'Inicio de sesion exitoso.',
                    'token': str(token),
                    'user': {
                        'id': user.id_usuario,
                        'nombre': user.usuario,
                        'correo': user.correo,
                        'rol': user.rol
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'message': 'Usuario o contrasena incorrectos.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                'message': f'Error en el servidor: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # ── ACTUALIZAR ─────────────────────────────────────────────
    @action(detail=False, methods=['put'], url_path='actualizar')
    def actualizar(self, request):
        id_usuario = request.data.get('id_usuario')
        if not id_usuario:
            return Response({'message': 'El campo id_usuario es obligatorio.'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            usuario = Usuario.objects.get(pk=id_usuario)
            # Campos actualizables
            if 'usuario' in request.data:
                usuario.usuario = request.data['usuario']
            if 'correo' in request.data:
                usuario.correo = request.data['correo']
            if 'rol' in request.data:
                usuario.rol = request.data['rol']
            if 'contrasena' in request.data and request.data['contrasena']:
                usuario.set_password(request.data['contrasena'])
            usuario.save()
            return Response({
                'message': f'Usuario "{usuario.usuario}" actualizado exitosamente.',
                'data': self.get_serializer(usuario).data
            }, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            return Response({'message': 'Usuario no encontrado.'},
                            status=status.HTTP_404_NOT_FOUND)

    # ── ANULAR (soft-delete) ───────────────────────────────────
    @action(detail=False, methods=['post'], url_path='anular')
    def anular(self, request):
        id_usuario = request.data.get('id_usuario')
        if not id_usuario:
            return Response({'message': 'El campo id_usuario es obligatorio.'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            usuario = Usuario.objects.get(pk=id_usuario)
            usuario.Estado = False
            usuario.save()
            return Response({
                'message': f'Usuario "{usuario.usuario}" anulado exitosamente.'
            }, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            return Response({'message': 'Usuario no encontrado.'},
                            status=status.HTTP_404_NOT_FOUND)

    # ── RESTAURAR ──────────────────────────────────────────────
    @action(detail=False, methods=['post'], url_path='restaurar')
    def restaurar(self, request):
        id_usuario = request.data.get('id_usuario')
        if not id_usuario:
            return Response({'message': 'El campo id_usuario es obligatorio.'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            usuario = Usuario.objects.get(pk=id_usuario)
            usuario.Estado = True
            usuario.save()
            return Response({
                'message': f'Usuario "{usuario.usuario}" restaurado exitosamente.'
            }, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            return Response({'message': 'Usuario no encontrado.'},
                            status=status.HTTP_404_NOT_FOUND)
