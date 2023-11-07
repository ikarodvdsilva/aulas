from django.db import models
from django.utils import timezone, formats
from .turmas import Turma
from django.db.models import Avg


class Aula(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    data = models.DateField()

    def __str__(self):
        if self.data:
            return formats.date_format(self.data, format="SHORT_DATE_FORMAT")
        else:
            return "No date available"

    def is_same_day_as_today(self):
        return self.data == timezone.now().date()

    def calcular_media_avaliacoes(self):
        if self.avaliacao_set.count() > 0:
            total_notas = sum(avaliacao.nota for avaliacao in self.avaliacao_set.all())
            media = total_notas / self.avaliacao_set.count()
            return round(media, 2)  # Arredonda a média para 2 casas decimais
        else:
            return "N/A"
