# Generated by Django 2.2.5 on 2019-10-08 13:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0012_config'),
    ]

    operations = [
        migrations.RenameField(
            model_name='config',
            old_name='multipliers',
            new_name='variables',
        ),
    ]
