# Generated by Django 2.2.8 on 2021-01-08 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qsar', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='descriptorgroup',
            name='corePackage',
            field=models.CharField(default='genui.models.genuimodels', max_length=1024),
        ),
    ]