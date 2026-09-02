from rest_framework import generics, status as http_status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Chamado
from .serializers import ChamadoSerializer


class ChamadoListCreateView(generics.ListCreateAPIView):
    """
    Lista e cria chamados.

    Correção INC-01: criação sem título retorna 400 (via serializer).
    Evolução INC-02: suporte a filtro por status via querystring,
    ex.: /api/chamados/?status=ABERTO
    """

    serializer_class = ChamadoSerializer

    def get_queryset(self):
        queryset = Chamado.objects.all().order_by("-criado_em")
        status_param = self.request.query_params.get("status")

        if status_param:
            status_param = status_param.strip().upper()
            valores_validos = [choice.value for choice in Chamado.Status]

            if status_param not in valores_validos:
                # Parâmetro inválido tratado de forma explícita (INC-02).
                raise ValueError(status_param)

            queryset = queryset.filter(status=status_param)

        return queryset

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except ValueError as exc:
            valores_validos = ", ".join(choice.value for choice in Chamado.Status)
            return Response(
                {
                    "detail": (
                        f"Status inválido: '{exc}'. "
                        f"Valores aceitos: {valores_validos}."
                    )
                },
                status=http_status.HTTP_400_BAD_REQUEST,
            )


class ChamadoDetailView(generics.RetrieveUpdateAPIView):
    queryset = Chamado.objects.all()
    serializer_class = ChamadoSerializer


class IndicadoresView(APIView):
    """
    Evolução INC-06: indicadores agregados de chamados.
    GET /api/indicadores/
    """

    def get(self, request, *args, **kwargs):
        total = Chamado.objects.count()
        abertos = Chamado.objects.filter(status=Chamado.Status.ABERTO).count()
        em_andamento = Chamado.objects.filter(
            status=Chamado.Status.EM_ANDAMENTO
        ).count()
        concluidos = Chamado.objects.filter(status=Chamado.Status.CONCLUIDO).count()

        return Response(
            {
                "total": total,
                "abertos": abertos,
                "em_andamento": em_andamento,
                "concluidos": concluidos,
            }
        )
