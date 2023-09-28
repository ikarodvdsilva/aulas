from django import forms
from django.contrib.auth.models import User
from .models import Aluno, Aula


class AlunoRegistroForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ["nome", "matricula"]


class AulaAdminForm(forms.ModelForm):
    class Meta:
        model = Aula
        fields = "__all__"
