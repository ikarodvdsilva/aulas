from django.contrib import admin

# Register your models here.
from .models import Aluno, Aula, Avaliacao, Disciplina, Turma

admin.site.register(Disciplina)
admin.site.register(Turma)
admin.site.register(Aula)
admin.site.register(Avaliacao)
admin.site.register(Aluno)
