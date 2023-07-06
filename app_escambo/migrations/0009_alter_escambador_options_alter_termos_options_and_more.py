# Generated by Django 4.2.3 on 2023-07-06 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_escambo', '0008_alter_escambador_endereco'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='escambador',
            options={'verbose_name_plural': 'Escambadores'},
        ),
        migrations.AlterModelOptions(
            name='termos',
            options={'verbose_name_plural': 'Termos'},
        ),
        migrations.AlterField(
            model_name='escambador',
            name='avaliacao',
            field=models.FloatField(default=5, verbose_name='Avaliação'),
        ),
    ]
