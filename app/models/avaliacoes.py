from django.db import models
from .alunos import Aluno
from .aulas import Aula
from .turmas import Turma


class Avaliacao(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)
    nota = models.FloatField()
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, null=True)
