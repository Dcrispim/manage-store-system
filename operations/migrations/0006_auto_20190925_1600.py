# Generated by Django 2.2.5 on 2019-09-25 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0005_auto_20190925_1550'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='itens',
        ),
        migrations.RemoveField(
            model_name='service',
            name='material',
        ),
    ]