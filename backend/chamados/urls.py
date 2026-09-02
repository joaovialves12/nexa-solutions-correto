from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChamadoViewSet

from .views import ChamadoDetailView, ChamadoListCreateView, IndicadoresView

urlpatterns = [
    path(
        "chamados/",
        ChamadoListCreateView.as_view(),
        name="chamado-list-create",
    ),
    path(
        "chamados/<int:pk>/",
        ChamadoDetailView.as_view(),
        name="chamado-detail",
    ),
    path(
        "indicadores/",
        IndicadoresView.as_view(),
        name="chamado-indicadores",
    ),
]
