from django.db import models
from django.utils import timezone, formats
from .turmas import Turma


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
