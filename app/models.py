from django.db import models
from django.contrib.auth.models import (
    User,
)


class Disciplina(models.Model):
    nome = models.CharField(max_length=100)


class Professor(models.Model):
    nome = models.CharField(max_length=100)


class Turma(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    alunos = models.ManyToManyField(User)
    professor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="ministra_aulas"
    )


class Aula(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    data = models.DateTimeField()


class Aluno(models.Model):
    nome = models.CharField(max_length=100, default="Digite seu nome aqui")
    matricula = models.CharField(max_length=10)
    senha = models.CharField(max_length=100)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nome


class Avaliacao(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)
    nota = models.FloatField()
