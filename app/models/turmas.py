from django.db import models
from .alunos import Aluno
from .disciplinas import Disciplina


class Turma(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    alunos = models.ManyToManyField(Aluno, related_name="turmas_turma")

    def __str__(self):
        return f"Turma de {self.disciplina.nome}"
