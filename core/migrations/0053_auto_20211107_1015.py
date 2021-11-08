# Generated by Django 3.2.7 on 2021-11-07 04:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0052_order_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='color',
            field=models.CharField(default='none', max_length=30),
        ),
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='cart',
            name='size',
            field=models.CharField(default='none', max_length=40),
        ),
        migrations.AlterField(
            model_name='cart',
            name='unit',
            field=models.CharField(default='none', max_length=30),
        ),
        migrations.AlterField(
            model_name='cart',
            name='unit_amount',
            field=models.FloatField(default=0),
        ),
    ]
