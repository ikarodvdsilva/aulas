from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from ..models import Aluno, Disciplina, Turma
from rest_framework import serializers
from django.http import JsonResponse


@csrf_exempt
def disciplinas(request, user_id):
    aluno = get_object_or_404(Aluno, id=user_id)
    turmas = Turma.objects.filter(alunos=aluno)
    disciplinas = Disciplina.objects.filter(turma__in=turmas)

    class DisciplinaSerializer(serializers.ModelSerializer):
        class Meta:
            model = Disciplina
            fields = "__all__"

    serializer = DisciplinaSerializer(disciplinas, many=True)
    serialized_disciplinas = serializer.data
    return JsonResponse({"disciplinas": serialized_disciplinas})
