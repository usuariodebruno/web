# Generated by Django 4.2.2 on 2023-07-15 02:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_escambo', '0003_mensagem_remetente'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='destaque',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='escambador',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='escambo/usuario_fotos'),
        ),
        migrations.AlterField(
            model_name='foto',
            name='imagem',
            field=models.ImageField(blank=True, null=True, upload_to='escambo/produto_fotos/'),
        ),
        migrations.AlterField(
            model_name='mensagem',
            name='remetente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_escambo.escambador'),
        ),
    ]
