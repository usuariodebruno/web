# Generated by Django 4.2.2 on 2023-07-11 02:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_escambo', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mensagem',
            name='remetente',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app_escambo.escambador'),
        ),
    ]