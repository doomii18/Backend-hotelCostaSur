from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from APPS.Categoria.models import Categoria
from APPS.Categoria.API.SerializerCategoria import SerializerCategoria


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all().order_by('id_categoria')
    serializer_class = SerializerCategoria

    # ── LISTAR (solo activas) ──────────────────────────────────
    @action(detail=False, methods=['get'], url_path='listar')
    def listar(self, request):
        categorias = Categoria.objects.filter(Estado=True).order_by('id_categoria')
        serializer = self.get_serializer(categorias, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # ── LISTAR TODOS (admin - activas e inactivas) ─────────────
    @action(detail=False, methods=['get'], url_path='listar-todos')
    def listar_todos(self, request):
        categorias = Categoria.objects.all().order_by('id_categoria')
        serializer = self.get_serializer(categorias, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # ── CREAR ──────────────────────────────────────────────────
    @action(detail=False, methods=['post'], url_path='crear')
    def crear(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            categoria = serializer.save()
            return Response({
                'message': f'Categoria "{categoria.NombreCategoria}" creada exitosamente.',
                'data': self.get_serializer(categoria).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ── ACTUALIZAR ─────────────────────────────────────────────
    @action(detail=False, methods=['put'], url_path='actualizar')
    def actualizar(self, request):
        id_categoria = request.data.get('id_categoria')
        if not id_categoria:
            return Response({'message': 'El campo id_categoria es obligatorio.'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            categoria = Categoria.objects.get(pk=id_categoria)
            serializer = self.get_serializer(categoria, data=request.data, partial=True)
            if serializer.is_valid():
                categoria = serializer.save()
                return Response({
                    'message': f'Categoria "{categoria.NombreCategoria}" actualizada exitosamente.',
                    'data': self.get_serializer(categoria).data
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Categoria.DoesNotExist:
            return Response({'message': 'Categoria no encontrada.'},
                            status=status.HTTP_404_NOT_FOUND)

    # ── ANULAR (soft-delete) ───────────────────────────────────
    @action(detail=False, methods=['post'], url_path='anular')
    def anular(self, request):
        id_categoria = request.data.get('id_categoria')
        if not id_categoria:
            return Response({'message': 'El campo id_categoria es obligatorio.'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            categoria = Categoria.objects.get(pk=id_categoria)
            categoria.Estado = False
            categoria.save()
            return Response({
                'message': f'Categoria "{categoria.NombreCategoria}" anulada exitosamente.'
            }, status=status.HTTP_200_OK)
        except Categoria.DoesNotExist:
            return Response({'message': 'Categoria no encontrada.'},
                            status=status.HTTP_404_NOT_FOUND)

    # ── RESTAURAR ──────────────────────────────────────────────
    @action(detail=False, methods=['post'], url_path='restaurar')
    def restaurar(self, request):
        id_categoria = request.data.get('id_categoria')
        if not id_categoria:
            return Response({'message': 'El campo id_categoria es obligatorio.'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            categoria = Categoria.objects.get(pk=id_categoria)
            categoria.Estado = True
            categoria.save()
            return Response({
                'message': f'Categoria "{categoria.NombreCategoria}" restaurada exitosamente.'
            }, status=status.HTTP_200_OK)
        except Categoria.DoesNotExist:
            return Response({'message': 'Categoria no encontrada.'},
                            status=status.HTTP_404_NOT_FOUND)
