# Generated by Django 2.2.8 on 2020-08-11 10:38

from django.db import migrations
from ..models import Map

def make_files(apps, schema_editor):
    for map in Map.objects.all():
        if not map.chemspaceJSON:
            print(f'Creating ChemSpace.js JSON file for map: {map.name}')
            map.saveChemSpaceJSON()

class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(make_files)
    ]