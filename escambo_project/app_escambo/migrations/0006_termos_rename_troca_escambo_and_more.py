# Generated by Django 4.2.2 on 2023-06-17 02:24

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('app_escambo', '0005_escambador_delete_usuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='Termos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf_file', models.FileField(upload_to='pdfs/')),
            ],
        ),
        migrations.RenameModel(
            old_name='Troca',
            new_name='Escambo',
        ),
        migrations.RenameField(
            model_name='produto',
            old_name='descricao',
            new_name='descricao_afetiva',
        ),
        migrations.RemoveField(
            model_name='chat',
            name='mensagens',
        ),
        migrations.AddField(
            model_name='chat',
            name='status_atividade',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='escambador',
            name='avaliacao',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='produto',
            name='estado_produto',
            field=models.CharField(choices=[('ruim', 'Ruim'), ('ok', 'Ok'), ('bom', 'Bom'), ('ótimo', 'Ótimo'), ('excelente', 'Excelente')], default='bom', max_length=20),
        ),
        migrations.AlterField(
            model_name='chat',
            name='participantes',
            field=models.ManyToManyField(blank=True, to='app_escambo.escambador'),
        ),
        migrations.AlterField(
            model_name='escambador',
            name='telefone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None),
        ),
        migrations.AlterField(
            model_name='escambo',
            name='usuario1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trocas1', to='app_escambo.escambador'),
        ),
        migrations.AlterField(
            model_name='escambo',
            name='usuario2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trocas2', to='app_escambo.escambador'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='usuario_proprietario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_escambo.escambador'),
        ),
        migrations.CreateModel(
            name='Mensagem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_hora', models.DateTimeField()),
                ('texto', models.CharField(max_length=2500)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_escambo.chat')),
            ],
        ),
        migrations.AddField(
            model_name='escambador',
            name='termos',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_escambo.termos'),
            preserve_default=False,
        ),
    ]