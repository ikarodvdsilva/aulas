from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import serializers
from ..models.disciplinas import Disciplina
from ..models.turmas import Turma


class DisciplinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disciplina
        fields = "__all__"


class TurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = "__all__"


@api_view(["GET"])
def detalhes_disciplina(request, disciplina_id):
    disciplina = get_object_or_404(Disciplina, pk=disciplina_id)
    turmas = Turma.objects.filter(disciplina=disciplina)
    disciplina_serializer = DisciplinaSerializer(disciplina)
    turma_serializer = TurmaSerializer(turmas, many=True)
    return Response(
        {
            "disciplina": disciplina_serializer.data,
            "turmas": turma_serializer.data,
        }
    )
