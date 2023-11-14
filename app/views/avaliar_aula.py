import datetime
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseForbidden
from ..models.alunos import Aluno
from ..models.aulas import Aula
from ..models.avaliacoes import Avaliacao
from django.db import IntegrityError
from django.http import JsonResponse
import json


@csrf_exempt
def avaliar_aula(request, user_id, aula_id, nota):
    try:
        aluno = get_object_or_404(Aluno, id=user_id)
        aula = get_object_or_404(Aula, pk=aula_id, turma__alunos=aluno)
        if datetime.datetime.now().date() != aula.data:
            return HttpResponseForbidden("Você só pode avaliar aulas do mesmo dia.")
        disciplina = aula.turma.disciplina
        if request.method == "POST":
            nota_str = nota
            if nota_str is None:
                return JsonResponse({"error": "Nota não fornecida."}, status=400)
            try:
                nota = float(nota_str)
            except ValueError:
                return JsonResponse(
                    {"error": "Nota fornecida não é um número válido."}, status=400
                )
            Avaliacao.objects.create(
                aluno=aluno, aula=aula, nota=nota, turma=aula.turma
            )
            return JsonResponse(
                {"message": "Avaliação criada com sucesso!"}, status=201
            )
        return render(
            request, "app/avaliar_aula.html", {"aula": aula, "disciplina": disciplina}
        )
    except IntegrityError:
        return JsonResponse(
            {"error": "Erro de integridade ao salvar a avaliação."}, status=500
        )
    except Exception as e:
        return JsonResponse({"error": f"Erro inesperado: {str(e)}"}, status=500)
