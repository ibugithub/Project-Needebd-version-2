# Generated by Django 3.1.13 on 2021-07-11 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0007_auto_20210711_1144'),
    ]

    operations = [
        migrations.AddField(
            model_name='voucheroffer',
            name='limit',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
