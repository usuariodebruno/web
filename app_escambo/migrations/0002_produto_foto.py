# Generated by Django 4.2.1 on 2023-05-31 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_escambo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='usuario_fotos/'),
        ),
    ]
