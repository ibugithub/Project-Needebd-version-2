# Generated by Django 3.2.7 on 2021-11-02 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0046_auto_20211102_0920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='MaximumUnitValue',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='MinimumUnitValue',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='unit',
            field=models.CharField(blank=True, choices=[('Kg', 'Kg'), ('Gram', 'Gram'), ('Pound', 'Pound'), ('Liter', 'Liter'), ('MiliLiter', 'MiliLiter')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='unitGroup',
            field=models.CharField(blank=True, choices=[('SolidWeight', 'SolidWeight'), ('LiquidWeight', 'LiquidWeight'), ('KgPacket', 'KgPacket'), ('LiterPacket', 'LiterPacket'), ('ClothSize', 'ClothSize'), ('ClothPicesSize', 'ClothPicesSize'), ('ShoeSize', 'ShoeSize'), ('Packet', 'Packet')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='unitValue',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]