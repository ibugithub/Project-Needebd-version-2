# Generated by Django 3.2.7 on 2021-10-09 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_customerprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerprofile',
            name='birthdate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='customerprofile',
            name='full_name',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='customerprofile',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], max_length=10, null=True),
        ),
    ]
