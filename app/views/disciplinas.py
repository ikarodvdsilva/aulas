from ..models import Aluno, Disciplina, Turma, Aula, Avaliacao
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from django.http import HttpResponseForbidden
from rest_framework.response import Response
from ..models import Aluno, Aula, Avaliacao
from ..serializers import AulaSerializer
from rest_framework import serializers
from django.db import IntegrityError
from django.http import JsonResponse
from ..forms import AlunoRegistroForm
import json


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
