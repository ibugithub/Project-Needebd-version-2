# Generated by Django 3.2.7 on 2021-11-20 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0061_ptattributevalue'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ptattributevalue',
            name='attributeValue',
        ),
        migrations.AddField(
            model_name='ptattributevalue',
            name='attribute',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.attribute'),
        ),
        migrations.DeleteModel(
            name='AttributeValue',
        ),
    ]
