# Generated by Django 3.2.7 on 2021-11-22 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0070_alter_order_delivery_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='singleProductCost',
            field=models.FloatField(null=True),
        ),
    ]