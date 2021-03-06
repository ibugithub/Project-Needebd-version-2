# Generated by Django 3.2.7 on 2021-11-22 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0065_auto_20211121_1121'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurierServices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('curierImage', models.ImageField(upload_to='curier_image')),
            ],
        ),
        migrations.RemoveField(
            model_name='attributevalue',
            name='attribute',
        ),
        migrations.RemoveField(
            model_name='attributevalue',
            name='attributeValueName',
        ),
        migrations.RemoveField(
            model_name='productattributevalue',
            name='product',
        ),
        migrations.RemoveField(
            model_name='ptattributevalue',
            name='attribute',
        ),
        migrations.RemoveField(
            model_name='ptattributevalue',
            name='attributeValue',
        ),
        migrations.RemoveField(
            model_name='ptattributevalue',
            name='productType',
        ),
        migrations.DeleteModel(
            name='Attribute',
        ),
        migrations.DeleteModel(
            name='AttributeValue',
        ),
        migrations.DeleteModel(
            name='ProductAttributeValue',
        ),
        migrations.DeleteModel(
            name='ProductType',
        ),
        migrations.DeleteModel(
            name='PTAttributeValue',
        ),
    ]
