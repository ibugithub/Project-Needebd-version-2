# Generated by Django 3.2.7 on 2021-11-24 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0079_auto_20211124_1138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='Total',
        ),
        migrations.RemoveField(
            model_name='order',
            name='subTotal',
        ),
    ]