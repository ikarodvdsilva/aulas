from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Aluno, Disciplina, Turma, Aula, Avaliacao
from django.contrib.auth.forms import UserCreationForm
from .forms import AlunoRegistroForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login
import json
from rest_framework import serializers
from django.contrib.auth.decorators import login_required
@csrf_exempt
@require_POST
def aluno_api(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        username = data.get("username")
        password = data.get("password")
        print(12)
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse(
                    {"status": "success", "message": "Login bem-sucedido."}
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


@login_required
def historico_aulas(request):
    aluno = "ikaro"
    print(11)
    turmas = Turma.objects.filter(alunos=aluno)
    aulas = Aula.objects.filter(turma__in=turmas)
    serialized_aulas = serializers.serialize("json", aulas)
    return JsonResponse({"aulas": json.loads(serialized_aulas)})


@login_required
def avaliar_aula(request, aula_id):
    aluno = request.user
    aula = Aula.objects.get(pk=aula_id, turma__alunos=aluno)

    if request.method == "POST":
        nota = float(request.POST.get("nota"))
        Avaliacao.objects.create(aluno=aluno, aula=aula, nota=nota)
        return redirect("historico_aulas")

    return render(request, "app/avaliar_aula.html", {"aula": aula})


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


def disciplinas(request):
    disciplinas = Disciplina.objects.all()
    serialized_disciplinas = serializers.serialize("json", disciplinas)
    return JsonResponse({"disciplinas": json.loads(serialized_disciplinas)})


def detalhes_disciplina(request, disciplina_id):
    disciplina = get_object_or_404(Disciplina, pk=disciplina_id)
    turmas = Turma.objects.filter(disciplina=disciplina)
    serialized_turmas = serializers.serialize("json", turmas)
    return JsonResponse(
        {
            "disciplina": json.loads(serializers.serialize("json", [disciplina])[1:-1]),
            "turmas": json.loads(serialized_turmas),
        }
    )


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
        print(user)

        if user is not None:
            login(request, user)

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Inclua o nome do usuário no payload do token
            access_token_payload = refresh.access_token.payload
            access_token_payload['username'] = user.username

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