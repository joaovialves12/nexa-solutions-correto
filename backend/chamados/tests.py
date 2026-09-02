from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Chamado

class ChamadoAPITests(APITestCase):

    def setUp(self):
        self.chamado1 = Chamado.objects.create(
            titulo="Erro de Login",
            descricao="Usuário não consegue entrar no sistema.",
            status="ABERTO"
        )
        self.chamado2 = Chamado.objects.create(
            titulo="Lentidão na consulta",
            descricao="A API de relatórios está demorando para responder.",
            status="CONCLUIDO"
        )
        self.url_list = reverse('chamado-list')

    def test_criar_chamado_valido(self):
        data = {
            "titulo": "Impressora sem papel",
            "descricao": "Adicionar resma no setor financeiro.",
            "status": "ABERTO"
        }
        response = self.client.post(self.url_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Chamado.objects.count(), 3)

    def test_validacao_titulo_curto(self):
        data = {
            "titulo": "Erro",
            "descricao": "Título com menos de 5 caracteres.",
            "status": "ABERTO"
        }
        response = self.client.post(self.url_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_endpoint_indicadores(self):
        url_indicadores = reverse('chamado-indicadores')
        response = self.client.get(url_indicadores)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total'], 2)
        self.assertEqual(response.data['abertos'], 1)
        self.assertEqual(response.data['concluidos'], 1)