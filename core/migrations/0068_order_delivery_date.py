# Generated by Django 3.2.7 on 2021-11-22 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0067_auto_20211122_1907'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_date',
            field=models.DateTimeField(null=True),
        ),
    ]
