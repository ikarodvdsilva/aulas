from .models.alunos import Aluno
from .models.aulas import Aula
from .models.turmas import Turma
from .models.avaliacoes import Avaliacao
from .models.disciplinas import Disciplina
from .models.professores import Professor
from django.utils.safestring import mark_safe
from app.forms import AulaAdminForm
from django.contrib import admin
from django.urls import reverse


class AvaliacaoInline(admin.TabularInline):
    model = Avaliacao
    extra = 0
    fields = ("aula", "nota")
    readonly_fields = ("aula", "nota")


class AulaInline(admin.TabularInline):
    model = Aula
    extra = 0
    fields = ("data",)
    readonly_fields = ("data",)


class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ("turma", "aula", "aluno", "nota")
    list_filter = ("turma__disciplina", "aula__data", "aluno")

    def turma(self, obj):
        return obj.aula.turma

    def aula(self, obj):
        return obj.aula.data

    def aluno(self, obj):
        return obj.aluno.nome

    actions = ["delete_selected"]

    def delete_selected(modeladmin, request, queryset):
        queryset.delete()

    delete_selected.short_description = "Excluir avaliações selecionadas"


class TurmaAdmin(admin.ModelAdmin):
    inlines = [AulaInline, AvaliacaoInline]
    list_display = ("__str__", "aulas_info")
    search_fields = ["disciplina__nome"]

    def aulas_info(self, obj):
        aulas_info = ", ".join(
            '<a href="{}">{}</a>'.format(
                reverse("admin:app_avaliacao_changelist"),
                str(aula),
            )
            for aula in obj.aula_set.all()
        )
        return mark_safe(aulas_info)

    aulas_info.short_description = "Aulas"


class AulaAdmin(admin.ModelAdmin):
    form = AulaAdminForm


admin.site.register(Aula, AulaAdmin)
admin.site.register(Avaliacao, AvaliacaoAdmin)
admin.site.register(Turma, TurmaAdmin)
admin.site.register(Disciplina)
admin.site.register(Aluno)
admin.site.register(Professor)
