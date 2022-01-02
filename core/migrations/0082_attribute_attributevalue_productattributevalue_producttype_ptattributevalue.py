# Generated by Django 3.2.7 on 2021-12-24 05:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0081_ordersummary_coupon_or_discount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attributeName', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attributeValueName', models.CharField(max_length=40)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.attribute')),
            ],
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeName', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='PTAttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attributeValue', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.attributevalue')),
                ('productType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.producttype')),
            ],
        ),
        migrations.CreateModel(
            name='ProductAttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attributeValue', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.attributevalue')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.product')),
            ],
        ),
    ]
