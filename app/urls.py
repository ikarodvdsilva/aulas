from django.urls import path
from .views.login_view import login_view
from .views.admin_dashboard import admin_dashboard
from .views.aluno_api import aluno_api
from .views.historico_aulas import historico_aulas
from .views.avaliar_aula import avaliar_aula
from .views.disciplinas import disciplinas
from .views.detalhes_disciplina import detalhes_disciplina
from .views.get_aulas import get_aulas

urlpatterns = [
    path("api/get-aulas/<int:user_id>/", get_aulas, name="get_aulas"),
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
