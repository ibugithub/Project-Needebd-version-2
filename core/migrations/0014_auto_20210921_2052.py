# Generated by Django 3.2.4 on 2021-09-21 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20210921_0915'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='size',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='unit_amount',
            field=models.IntegerField(null=True),
        ),
    ]
