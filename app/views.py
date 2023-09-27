from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Disciplina, Turma, Aula, Avaliacao
from django.contrib.auth.forms import UserCreationForm
from .forms import AlunoRegistroForm


@login_required
def historico_aulas(request):
    aluno = request.user
    turmas = Turma.objects.filter(alunos=aluno)
    aulas = Aula.objects.filter(turma__in=turmas)
    return render(request, "historico_aulas.html", {"aulas": aulas})


@login_required
def avaliar_aula(request, aula_id):
    aluno = request.user
    aula = Aula.objects.get(pk=aula_id, turma__alunos=aluno)

    if request.method == "POST":
        nota = float(request.POST.get("nota"))
        Avaliacao.objects.create(aluno=aluno, aula=aula, nota=nota)
        return redirect("historico_aulas")

    return render(request, "avaliar_aula.html", {"aula": aula})


@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect("login")

    disciplinas = Disciplina.objects.all()
    turmas = Turma.objects.all()
    aulas = Aula.objects.all()

    return render(
        request,
        "admin_dashboard.html",
        {"disciplinas": disciplinas, "turmas": turmas, "aulas": aulas},
    )


def disciplinas(request):
    disciplinas = Disciplina.objects.all()
    return render(request, "app/disciplinas.html", {"disciplinas": disciplinas})


def detalhes_disciplina(request, disciplina_id):
    disciplina = get_object_or_404(Disciplina, pk=disciplina_id)
    turmas = Turma.objects.filter(disciplina=disciplina)
    return render(
        request,
        "app/detalhes_disciplina.html",
        {"disciplina": disciplina, "turmas": turmas},
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
