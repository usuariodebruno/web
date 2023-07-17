# Generated by Django 4.2.2 on 2023-07-16 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_escambo', '0007_escambo_confirmado_usuario1_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='escambo',
            old_name='confirmado_usuario1',
            new_name='confirmado_usuario_iniciou',
        ),
        migrations.RenameField(
            model_name='escambo',
            old_name='confirmado_usuario2',
            new_name='confirmado_usuario_outro',
        ),
        migrations.AddField(
            model_name='escambo',
            name='usuario_iniciou',
            field=models.IntegerField(default=123),
        ),
    ]