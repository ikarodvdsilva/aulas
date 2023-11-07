from django.db.models import Avg
from django.db import models
from .alunos import Aluno
from .aulas import Aula
from .turmas import Turma


class Avaliacao(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)
    nota = models.FloatField()
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, null=True)

    def calcular_media_avaliacoes(self):
        media = self.avaliacao_set.aggregate(media_avaliacao=Avg("nota"))
        return media["media_avaliacao"]
