# Generated by Django 2.2.5 on 2019-10-15 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0013_auto_20191008_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='off',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=5, null=True),
        ),
    ]
