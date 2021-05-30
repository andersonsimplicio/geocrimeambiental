# Generated by Django 3.1.3 on 2021-05-29 10:58

from django.db import migrations, models
import geo.models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0008_auto_20210529_0756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processo',
            name='arquivo',
            field=models.FileField(blank=True, default=None, null=True, upload_to=geo.models.user_directory_path),
        ),
        migrations.AlterField(
            model_name='processo',
            name='cod_floresta',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='processo',
            name='cod_municipio_ibge',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='processo',
            name='cod_sigef',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='processo',
            name='latitude',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='processo',
            name='longitude',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='processo',
            name='sicar',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='processo',
            name='sirenejud',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='processo',
            name='terrai_cod',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
    ]
