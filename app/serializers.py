from django.core.serializers import serialize
from .models import Aluno


class AlunoSerializer:
    def to_json(self, alunos):
        return serialize("json", alunos)
