from .models import Aluno, Disciplina, Turma, Aula, Avaliacao
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
from .models import Aluno, Aula, Avaliacao
from .serializers import AulaSerializer
from rest_framework import serializers
from django.db import IntegrityError
from django.http import JsonResponse
from .forms import AlunoRegistroForm
import json


@csrf_exempt
@require_POST
def aluno_api(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                access_token_payload = refresh.access_token.payload
                access_token_payload["username"] = user.username
                return JsonResponse(
                    {
                        "status": "success",
                        "message": "Login bem-sucedido.",
                        "access_token": str(access_token_payload),
                    }
                )
            else:
                return JsonResponse(
                    {"status": "error", "message": "Credenciais inválidas."}, status=401
                )
        else:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Nome de usuário e senha são obrigatórios.",
                },
                status=400,
            )
    except json.JSONDecodeError:
        return JsonResponse(
            {"status": "error", "message": "Erro ao decodificar o JSON."}, status=400
        )


@api_view(["GET"])
def historico_aulas(request, user_id):
    aluno = get_object_or_404(Aluno, id=user_id)
    turmas = Turma.objects.filter(alunos=aluno)
    aulas = Aula.objects.filter(turma__in=turmas)
    serializer = AulaSerializer(aulas, many=True)
    return Response({"aulas": serializer.data})


@csrf_exempt
def avaliar_aula(request, user_id, aula_id, nota):
    try:
        aluno = get_object_or_404(Aluno, id=user_id)
        aula = get_object_or_404(Aula, pk=aula_id, turma__alunos=aluno)
        if not aula.is_same_day_as_today():
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


class DisciplinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disciplina
        fields = "__all__"


class TurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = "__all__"


def registrar_aluno(request):
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        aluno_form = AlunoRegistroForm(request.POST)

        if user_form.is_valid() and aluno_form.is_valid():
            user = user_form.save()
            aluno = aluno_form.save(commit=False)
            aluno.user = user
            aluno.save()

    else:
        user_form = UserCreationForm()
        aluno_form = AlunoRegistroForm()

    return render(
        request,
        "app/registrar_aluno.html",
        {"user_form": user_form, "aluno_form": aluno_form},
    )


@csrf_exempt
@require_POST
def login_view(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        username = data.get("username")
        password = data.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            access_token_payload = refresh.access_token.payload
            access_token_payload["username"] = user.username
            return JsonResponse(
                {
                    "status": "success",
                    "message": "Login bem-sucedido.",
                    "access_token": str(access_token_payload),
                }
            )
        else:
            return JsonResponse(
                {"status": "error", "message": "Credenciais inválidas."},
                status=401,
            )
    except json.JSONDecodeError:
        return JsonResponse(
            {"status": "error", "message": "Erro ao decodificar o JSON."},
            status=400,
        )
