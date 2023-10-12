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
    path("api/historico/<int:user_id>", historico_aulas, name="historico_aulas"),
    path(
        "api/avaliar-aulas/<int:user_id>/<int:aula_id>/<int:nota>/",
        avaliar_aula,
        name="avaliar_aula",
    ),
    path("api/disciplinas/<int:user_id>/", disciplinas, name="disciplinas"),
    path(
        "api/disciplina/<int:disciplina_id>/",
        detalhes_disciplina,
        name="detalhes_disciplina",
    ),
]
