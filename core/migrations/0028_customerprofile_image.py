# Generated by Django 3.2.7 on 2021-10-09 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_customerprofile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerprofile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='customerimages'),
        ),
    ]
