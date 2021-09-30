# Generated by Django 3.2.4 on 2021-09-21 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20210921_0852'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Kg_Unit',
        ),
        migrations.AddField(
            model_name='product',
            name='unit',
            field=models.CharField(blank=True, choices=[('Kg', 'kg'), ('Liter', 'Liter'), ('Size', 'Size')], max_length=30, null=True),
        ),
    ]
