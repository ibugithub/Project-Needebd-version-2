# Generated by Django 3.2.7 on 2021-12-24 05:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0082_attribute_attributevalue_productattributevalue_producttype_ptattributevalue'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='ProductType',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.producttype'),
        ),
    ]
