# Generated by Django 3.2.7 on 2021-10-18 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_customeraddress_isdefault'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customeraddress',
            name='isDefault',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
