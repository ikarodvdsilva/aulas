# app/urls.py

from django.urls import path
from .views import (
    aluno_api,
    detalhes_disciplina,
    disciplinas,
    historico_aulas,
    avaliar_aula,
    admin_dashboard,
    login_view,
)

urlpatterns = [
    path("api/login/", login_view, name="login_view"),
    path("api/alunos/", aluno_api, name="aluno_api"),
    path("admin/", admin_dashboard, name="admin_dashboard"),
    path("api/historico/", historico_aulas, name="historico_aulas"),
    path("avaliar/<int:aula_id>/", avaliar_aula, name="avaliar_aula"),
    path("disciplinas/", disciplinas, name="disciplinas"),
    path(
        "disciplina/<int:disciplina_id>/",
        detalhes_disciplina,
        name="detalhes_disciplina",
    ),
]
