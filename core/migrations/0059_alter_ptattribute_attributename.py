# Generated by Django 3.2.7 on 2021-11-20 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0058_producttype_ptattribute_ptattributevalue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ptattribute',
            name='attributeName',
            field=models.CharField(max_length=40),
        ),
    ]
