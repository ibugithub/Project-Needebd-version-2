# Generated by Django 3.2.7 on 2021-11-05 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0048_alter_product_discount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='unitValue',
            new_name='unitValue_On_Increase_or_Decrease',
        ),
    ]
