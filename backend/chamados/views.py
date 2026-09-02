from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Chamado
from .serializers import ChamadoSerializer

class ChamadoViewSet(viewsets.ModelViewSet):
    queryset = Chamado.objects.all().order_by('-criado_em')
    serializer_class = ChamadoSerializer

    @action(detail=False, methods=['get'])
    def indicadores(self, request):
        total = Chamado.objects.count()
        abertos = Chamado.objects.filter(status='ABERTO').count()
        em_andamento = Chamado.objects.filter(status='EM_ANDAMENTO').count()
        concluidos = Chamado.objects.filter(status='CONCLUIDO').count()

        return Response({
            'total': total,
            'abertos': abertos,
            'em_andamento': em_andamento,
            'concluidos': concluidos,
        }, status=status.HTTP_200_OK)