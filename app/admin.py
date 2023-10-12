from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from app.forms import AulaAdminForm
from .models import Aluno, Aula, Avaliacao, Disciplina, Professor, Turma


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

    # Adiciona a ação em lote para excluir avaliações selecionadas
    actions = ["delete_selected"]

    def delete_selected(modeladmin, request, queryset):
        # Exclui todas as avaliações selecionadas
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
