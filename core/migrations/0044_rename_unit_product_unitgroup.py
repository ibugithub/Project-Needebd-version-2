# Generated by Django 3.2.7 on 2021-11-01 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0043_alter_product_unit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='unit',
            new_name='unitGroup',
        ),
    ]