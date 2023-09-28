from django.db import models
from django.contrib.auth.models import User
from django.utils import formats


class Disciplina(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Professor(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Turma(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    alunos = models.ManyToManyField("Aluno", related_name="turmas_turma")

    def __str__(self):
        return f"Turma de {self.disciplina.nome}"


class Aula(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    data = models.DateTimeField()

    def __str__(self):
        return formats.date_format(self.data, format="SHORT_DATETIME_FORMAT")


class Aluno(models.Model):
    nome = models.CharField(max_length=100, default="Digite seu nome aqui")
    matricula = models.CharField(max_length=10)
    senha = models.CharField(max_length=100)
    turma = models.ForeignKey(
        Turma, on_delete=models.CASCADE, null=True, related_name="turmas_aluno"
    )

    def __str__(self):
        return self.nome


class Avaliacao(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)
    nota = models.FloatField()
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, default=1)
