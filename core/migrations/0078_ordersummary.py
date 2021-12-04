# Generated by Django 3.2.7 on 2021-11-24 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0077_delete_ordersummary'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderSummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subTotal', models.FloatField()),
                ('total', models.FloatField()),
                ('orderItem', models.ManyToManyField(to='core.Order')),
            ],
        ),
    ]
