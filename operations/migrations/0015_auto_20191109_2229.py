# Generated by Django 2.2.5 on 2019-11-09 22:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0014_auto_20191015_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='sbid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart_sb', to='operations.SalesOrBuy'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='svid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart_s', to='operations.Service'),
        ),
    ]
