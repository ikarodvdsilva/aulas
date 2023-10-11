from django.db import models
from django.contrib.auth.models import User
from django.utils import formats
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
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

    def __str__(self):
        return self.nome


@receiver(post_save, sender=Aluno)
def create_user_for_aluno(sender, instance, created, **kwargs):
    if created:
        user = User.objects.create_user(
            username=instance.nome,
            password=instance.senha,
        )
        instance.user = user
        instance.save()


class Avaliacao(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)
    nota = models.FloatField()
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, default=1)
