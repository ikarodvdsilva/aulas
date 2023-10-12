from django.db import models


class Aluno(models.Model):
    nome = models.CharField(max_length=100, default="Digite seu nome aqui")
    matricula = models.CharField(max_length=10)
    senha = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
