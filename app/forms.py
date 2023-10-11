from django import forms
from django.contrib.auth.models import User
from .models import Aluno, Aula
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class AlunoRegistroForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ["nome", "matricula"]


class AulaAdminForm(forms.ModelForm):
    class Meta:
        model = Aula
        fields = "__all__"


class CustomUserCreationForm(UserCreationForm):
    is_aluno = forms.BooleanField(required=False)
    is_professor = forms.BooleanField(required=False)

    class Meta:
        model = CustomUser
        fields = ["username", "password1", "password2", "is_aluno", "is_professor"]
