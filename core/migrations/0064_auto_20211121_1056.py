# Generated by Django 3.2.7 on 2021-11-21 04:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0063_productattributevalue'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attributeValueName', models.CharField(max_length=20)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.attribute')),
            ],
        ),
        migrations.AddField(
            model_name='ptattributevalue',
            name='attributeValue',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.attributevalue'),
        ),
    ]
