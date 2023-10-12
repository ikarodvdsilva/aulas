from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone, formats
from app.models.alunos import Aluno
from app.models.professores import Professor


class CustomUser(AbstractUser):
    is_aluno = models.BooleanField(default=False)
    is_professor = models.BooleanField(default=False)


CustomUser._meta.get_field("groups").remote_field.related_name = "customuser_groups"
CustomUser._meta.get_field(
    "user_permissions"
).remote_field.related_name = "customuser_user_permissions"


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
