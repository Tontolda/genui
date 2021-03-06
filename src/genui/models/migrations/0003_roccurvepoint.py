# Generated by Django 2.2.8 on 2020-05-15 13:25

from django.db import migrations, models
import django.db.models.deletion
import genui.utils.models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0002_auto_20200505_0727'),
    ]

    operations = [
        migrations.CreateModel(
            name='ROCCurvePoint',
            fields=[
                ('modelperformance_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='models.ModelPerformance')),
                ('fpr', models.FloatField()),
                ('auc', models.ForeignKey(on_delete=genui.utils.models.NON_POLYMORPHIC_CASCADE, related_name='points', to='models.ModelPerformance')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('models.modelperformance',),
        ),
    ]
