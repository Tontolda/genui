# Generated by Django 2.2.8 on 2020-04-27 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('compounds', '0001_initial'),
        ('qsar', '__first__'),
        ('modelling', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Map',
            fields=[
                ('model_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='modelling.Model')),
                ('molsets', models.ManyToManyField(related_name='maps', to='compounds.MolSet')),
            ],
            options={
                'abstract': False,
            },
            bases=('modelling.model',),
        ),
        migrations.CreateModel(
            name='MappingStrategy',
            fields=[
                ('trainingstrategy_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='modelling.TrainingStrategy')),
                ('descriptors', models.ManyToManyField(to='qsar.DescriptorGroup')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('modelling.trainingstrategy',),
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
                ('map', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maps.Map')),
                ('molecule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compounds.Molecule')),
            ],
            options={
                'unique_together': {('map', 'molecule')},
            },
        ),
    ]
