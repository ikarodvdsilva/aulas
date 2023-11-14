import datetime
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import serializers
from django.views.decorators.csrf import csrf_exempt

from app.models.aulas import Aula
from app.serializers import AulaSerializer
from ..models.disciplinas import Disciplina
from ..models.turmas import Turma


@csrf_exempt
@api_view(["GET"])
def get_aulas(request, user_id):
    # Obtenha todas as aulas associadas ao aluno
    aulas = Aula.objects.filter(turma__alunos__id=user_id)

    # Serializar a lista de aulas
    serializer = AulaSerializer(aulas, many=True)

    # Retornar a lista serializada como resposta
    return Response(serializer.data)
