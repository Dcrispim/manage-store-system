# Generated by Django 2.2.5 on 2019-09-25 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesorbuy',
            name='off',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=3),
        ),
    ]
