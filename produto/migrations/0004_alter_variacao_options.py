# Generated by Django 4.2.2 on 2023-06-29 01:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0003_variacao'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='variacao',
            options={'verbose_name': 'Variação', 'verbose_name_plural': 'Variações'},
        ),
    ]