from django.core.serializers import serialize
from .models import Aluno
from .models import Aula, Turma
from rest_framework import serializers


class AlunoSerializer:
    def to_json(self, alunos):
        return serialize("json", alunos)


class AulaSerializer(serializers.ModelSerializer):
    disciplina_nome = serializers.SerializerMethodField()

    class Meta:
        model = Aula
        fields = ["data", "disciplina_nome"]

    def get_disciplina_nome(self, obj):
        return obj.turma.disciplina.nome
