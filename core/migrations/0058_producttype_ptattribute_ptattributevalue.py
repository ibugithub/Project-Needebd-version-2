# Generated by Django 3.2.7 on 2021-11-20 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0057_auto_20211119_1802'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeName', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='PTAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attributeName', models.CharField(max_length=20)),
                ('productType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.producttype')),
            ],
        ),
        migrations.CreateModel(
            name='PTAttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ptAttributeValue', models.FloatField()),
                ('ptAttribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.ptattribute')),
            ],
        ),
    ]
