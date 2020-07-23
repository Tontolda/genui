# Generated by Django 2.2.8 on 2020-07-16 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('compounds', '0004_molsetfile'),
    ]

    operations = [
        migrations.CreateModel(
            name='CSVCompounds',
            fields=[
                ('molset_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='compounds.MolSet')),
                ('nameCol', models.CharField(default='NAME', max_length=256, null=True)),
                ('smilesCol', models.CharField(default='SMILES', max_length=256)),
                ('activityCol', models.CharField(default='ACTIVITY', max_length=256)),
                ('activityTypeCol', models.CharField(default='ACTIVITY_TYPE', max_length=256)),
                ('activityUnitCol', models.CharField(default='ACTIVITY_UNIT', max_length=256, null=True)),
                ('colSeparator', models.CharField(default=',', max_length=1)),
                ('emptyValue', models.CharField(blank=True, default='NA', max_length=1)),
            ],
            options={
                'abstract': False,
            },
            bases=('compounds.molset',),
        ),
        migrations.CreateModel(
            name='CSVMolecule',
            fields=[
                ('molecule_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='compounds.Molecule')),
                ('name', models.CharField(blank=True, max_length=1024)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('compounds.molecule',),
        ),
    ]