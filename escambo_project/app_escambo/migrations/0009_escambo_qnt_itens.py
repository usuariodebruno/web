# Generated by Django 4.2.2 on 2023-07-16 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_escambo', '0008_rename_confirmado_usuario1_escambo_confirmado_usuario_iniciou_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='escambo',
            name='qnt_itens',
            field=models.IntegerField(default=0),
        ),
    ]
