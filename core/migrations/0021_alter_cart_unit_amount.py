# Generated by Django 3.2.7 on 2021-10-01 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20211001_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='unit_amount',
            field=models.FloatField(null=True),
        ),
    ]