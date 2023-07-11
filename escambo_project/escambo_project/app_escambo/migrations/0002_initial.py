# Generated by Django 4.2.2 on 2023-07-11 00:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_escambo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Cesta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obsvacoes', models.CharField(blank=True, max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_atividade', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Escambador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpf', models.CharField(blank=True, max_length=14)),
                ('endereco', models.CharField(max_length=255)),
                ('telefone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='static/escambo/usuario_fotos')),
                ('avaliacao', models.FloatField(default=5)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao_afetiva', models.CharField(max_length=500)),
                ('estado_produto', models.CharField(choices=[('ruim', 'Ruim'), ('ok', 'Ok'), ('bom', 'Bom'), ('ótimo', 'Ótimo'), ('excelente', 'Excelente')], default='bom', max_length=20)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_escambo.categoria')),
                ('usuario_proprietario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_escambo.escambador')),
            ],
        ),
        migrations.CreateModel(
            name='Mensagem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_hora', models.DateTimeField(default=django.utils.timezone.now)),
                ('texto', models.CharField(max_length=2500)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_escambo.chat')),
            ],
        ),
        migrations.CreateModel(
            name='Foto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='static/escambo/produto_fotos/')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_escambo.produto')),
            ],
        ),
        migrations.CreateModel(
            name='Escambo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_escambo', models.BooleanField(default=True)),
                ('cestas', models.ManyToManyField(to='app_escambo.cesta')),
                ('chat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_escambo.chat')),
                ('usuarios', models.ManyToManyField(to='app_escambo.escambador')),
            ],
        ),
        migrations.AddField(
            model_name='chat',
            name='usuarios',
            field=models.ManyToManyField(to='app_escambo.escambador'),
        ),
        migrations.AddField(
            model_name='cesta',
            name='escambador_dono',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_escambo.escambador'),
        ),
        migrations.AddField(
            model_name='cesta',
            name='produto',
            field=models.ManyToManyField(to='app_escambo.produto'),
        ),
    ]
