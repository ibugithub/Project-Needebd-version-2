# Generated by Django 3.2.7 on 2021-11-22 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0071_order_singleproductcost'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shippingCost',
            field=models.FloatField(null=True),
        ),
    ]
