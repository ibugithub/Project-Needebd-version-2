# Generated by Django 3.2.7 on 2021-11-22 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0066_auto_20211122_1317'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CurierServices',
            new_name='CourierServices',
        ),
        migrations.RenameField(
            model_name='courierservices',
            old_name='curierImage',
            new_name='courierImage',
        ),
        migrations.AddField(
            model_name='order',
            name='courier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.courierservices'),
        ),
    ]
