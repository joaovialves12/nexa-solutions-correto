from rest_framework import serializers
from .models import Chamado


class ChamadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chamado
        fields = [
            "id",
            "titulo",
            "descricao",
            "status",
            "criado_em",
            "atualizado_em",
        ]
        read_only_fields = [
            "id",
            "criado_em",
            "atualizado_em",
        ]
        # Correção INC-01:
        # título passa a ser obrigatório e não pode ser vazio/em branco.
        extra_kwargs = {
            "titulo": {
                "required": True,
                "allow_blank": False,
            },
        }

    def validate_titulo(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("O campo 'titulo' é obrigatório.")
        return value.strip()
