# Generated by Django 3.2.4 on 2021-08-30 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0016_auto_20210712_0631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='voucher',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='voucheroffer',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
