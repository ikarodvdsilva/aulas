from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils import timezone
from django.utils import formats
from django.db import models


class CustomUser(AbstractUser):
    is_aluno = models.BooleanField(default=False)
    is_professor = models.BooleanField(default=False)


CustomUser._meta.get_field("groups").remote_field.related_name = "customuser_groups"
CustomUser._meta.get_field(
    "user_permissions"
).remote_field.related_name = "customuser_user_permissions"


class Disciplina(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Professor(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Aluno(models.Model):
    nome = models.CharField(max_length=100, default="Digite seu nome aqui")
    matricula = models.CharField(max_length=10)
    senha = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Turma(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    alunos = models.ManyToManyField(Aluno, related_name="turmas_turma")

    def __str__(self):
        return f"Turma de {self.disciplina.nome}"


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


@receiver(post_save, sender=Professor)
def create_user_for_professor(sender, instance, created, **kwargs):
    if created:
        user = User.objects.create_user(
            username=instance.nome,
            password="123456",
        )
        instance.user = user
        instance.save()


@receiver(post_save, sender=Aluno)
def create_user_for_aluno(sender, instance, created, **kwargs):
    if created:
        user = User.objects.create_user(
            username=instance.nome,
            password=instance.senha,
            id=instance.id,
        )
        instance.user = user
        instance.save()


class Avaliacao(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)
    nota = models.FloatField()
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, null=True)
