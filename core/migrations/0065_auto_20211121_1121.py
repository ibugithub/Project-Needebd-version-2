# Generated by Django 3.2.7 on 2021-11-21 05:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0064_auto_20211121_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attributevalue',
            name='attributeValueName',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.productattributevalue'),
        ),
        migrations.AlterField(
            model_name='productattributevalue',
            name='PTAttributeValue',
            field=models.CharField(max_length=20),
        ),
    ]