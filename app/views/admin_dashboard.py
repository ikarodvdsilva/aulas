from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ..models import Disciplina, Turma, Aula
from rest_framework import serializers
import json


@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return JsonResponse(
            {"status": "error", "message": "Usuário não autorizado"}, status=403
        )
    disciplinas = Disciplina.objects.all()
    turmas = Turma.objects.all()
    aulas = Aula.objects.all()
    serialized_disciplinas = serializers.serialize("json", disciplinas)
    serialized_turmas = serializers.serialize("json", turmas)
    serialized_aulas = serializers.serialize("json", aulas)
    return JsonResponse(
        {
            "disciplinas": json.loads(serialized_disciplinas),
            "turmas": json.loads(serialized_turmas),
            "aulas": json.loads(serialized_aulas),
        }
    )
