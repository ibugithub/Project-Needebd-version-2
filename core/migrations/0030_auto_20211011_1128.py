# Generated by Django 3.2.7 on 2021-10-11 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_alter_customerprofile_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Districts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('division_id', models.IntegerField()),
                ('name', models.CharField(max_length=40)),
                ('bn_name', models.CharField(max_length=25, null=True)),
                ('lat', models.CharField(max_length=15, null=True)),
                ('lon', models.CharField(max_length=15, null=True)),
                ('url', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Divisions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('bn_name', models.CharField(max_length=25)),
                ('url', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Unions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upazilla_id', models.IntegerField()),
                ('name', models.CharField(max_length=25)),
                ('bn_name', models.CharField(max_length=25)),
                ('url', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Upazilas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('district_id', models.IntegerField()),
                ('name', models.CharField(max_length=25)),
                ('bn_name', models.CharField(max_length=25)),
                ('url', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='customerprofile',
            name='birthdate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customerprofile',
            name='gender',
            field=models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], max_length=10, null=True),
        ),
    ]