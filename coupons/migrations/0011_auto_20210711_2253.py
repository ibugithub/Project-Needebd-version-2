# Generated by Django 3.1.13 on 2021-07-11 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0010_auto_20210711_2252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voucher',
            name='count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
