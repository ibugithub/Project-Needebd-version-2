# Generated by Django 3.2.7 on 2021-10-07 06:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_auto_20211007_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_wraper',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.categorywraper'),
        ),
        migrations.AlterField(
            model_name='category',
            name='display_wraper',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.displaywraper'),
        ),
    ]
