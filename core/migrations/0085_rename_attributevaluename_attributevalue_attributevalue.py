# Generated by Django 3.2.7 on 2021-12-24 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0084_productattributevalue_productstock'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attributevalue',
            old_name='attributeValueName',
            new_name='attributeValue',
        ),
    ]
