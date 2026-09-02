from django.db import models


class Chamado(models.Model):
    class Status(models.TextChoices):
        ABERTO = "ABERTO", "Aberto"
        EM_ANDAMENTO = "EM_ANDAMENTO", "Em andamento"
        CONCLUIDO = "CONCLUIDO", "Concluído"

    # Correção INC-01: título é obrigatório (não pode ficar em branco).
    titulo = models.CharField(max_length=150, blank=False)

    descricao = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ABERTO,
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-criado_em"]

    def __str__(self):
        return self.titulo
