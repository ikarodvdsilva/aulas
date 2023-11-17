import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from django.views.decorators.csrf import csrf_exempt
from app.models.aulas import Aula
from app.serializers import AulaSerializer


@csrf_exempt
@api_view(["GET"])
def get_aulas(request, user_id):
    aulas = Aula.objects.filter(turma__alunos__id=user_id)
    serializer = AulaSerializer(aulas, many=True)
    return Response(serializer.data)
