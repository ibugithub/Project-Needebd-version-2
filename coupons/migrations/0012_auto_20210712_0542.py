# Generated by Django 3.1.13 on 2021-07-11 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0011_auto_20210711_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voucher',
            name='count',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
