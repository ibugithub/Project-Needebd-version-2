# Generated by Django 3.2.7 on 2021-10-07 06:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0020_auto_20211007_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voucheroffer',
            name='limit',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
