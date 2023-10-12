from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Aluno, Aula, Turma
from ..serializers import AulaSerializer


@api_view(["GET"])
def historico_aulas(request, user_id):
    aluno = get_object_or_404(Aluno, id=user_id)
    turmas = Turma.objects.filter(alunos=aluno)
    aulas = Aula.objects.filter(turma__in=turmas)
    serializer = AulaSerializer(aulas, many=True)
    return Response({"aulas": serializer.data})
