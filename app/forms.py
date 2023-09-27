from django import forms
from django.contrib.auth.models import User
from .models import Aluno


class AlunoRegistroForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ["nome", "matricula"]
