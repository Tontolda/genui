"""
tasks

Created by: Martin Sicho
On: 18-12-19, 13:14
"""
from celery import shared_task

from commons.tasks import ProgressRecorder
from .models import MolSet
from . import initializers

@shared_task(name='CreateCompoundSet', bind=True)
def populateMolSet(self, molset_id, initializer_class, initializer_kwargs=None):
    if not initializer_kwargs:
        initializer_kwargs = dict()
    instance = MolSet.objects.get(pk=molset_id)
    initializer_class = getattr(initializers, initializer_class)
    initializer = initializer_class(instance, ProgressRecorder(self), **initializer_kwargs)
    count = initializer.populateInstance()
    return {
        "populationSize" : count
        , "errors" : [repr(x) for x in initializer.errors]
    }

@shared_task(name='UpdateCompoundSet', bind=True)
def updateMolSet(self, molset_id, updater_class, updater_kwargs=None):
    if not updater_kwargs:
        updater_kwargs = dict()
    instance = MolSet.objects.get(pk=molset_id)
    updater_class = getattr(initializers, updater_class)
    updater = updater_class(instance, ProgressRecorder(self), **updater_kwargs)
    count = updater.updateInstance()
    return {
        "populationSize" : count
        , "errors" : [repr(x) for x in updater.errors]
    }