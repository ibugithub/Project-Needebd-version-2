# Generated by Django 3.2.7 on 2021-12-28 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0086_remove_product_productgroup'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='unit',
        ),
        migrations.AlterField(
            model_name='productattributevalue',
            name='attributeValue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.attributevalue'),
        ),
    ]
