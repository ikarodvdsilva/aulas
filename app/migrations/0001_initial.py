# Generated by Django 4.2.5 on 2023-09-27 11:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Aula",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("data", models.DateTimeField()),
                ("nota", models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Disciplina",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Turma",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("alunos", models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                (
                    "disciplina",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.disciplina"
                    ),
                ),
                (
                    "professor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ministra_aulas",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Avaliacao",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nota", models.FloatField()),
                (
                    "aluno",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "aula",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.aula"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="aula",
            name="turma",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="app.turma"
            ),
        ),
    ]