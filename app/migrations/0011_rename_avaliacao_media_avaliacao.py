# Generated by Django 4.2.5 on 2023-09-27 23:57

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0010_avaliacao_turma"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Avaliacao",
            new_name="Media_Avaliacao",
        ),
    ]