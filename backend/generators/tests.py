import json
import os

from django.urls import reverse
from rest_framework.test import APITestCase, APITransactionTestCase

from generators.core import builders
from generators.models import DrugExNet, DrugExAgent, Generator, GeneratedMolSet
from modelling.models import Algorithm, AlgorithmMode, ModelFile, Model
from qsar.tests import InitMixIn
from compounds import initializers

TEST_EPOCHS = 1

class SetUpDrugExGeneratorsMixIn(InitMixIn):

    def getPerformance(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        print(json.dumps(response.data, indent=4))
        return response

    def createGenerator(self, create_url, initial=None):
        post_data = {
          "name": "Test DrugEx Network",
          "description": "test description",
          "project": self.project.id,
          "trainingStrategy": {
            "algorithm": Algorithm.objects.get(name="DrugExNetwork").id,
            "mode": AlgorithmMode.objects.get(name="generator").id,
            "parameters": {
                "nEpochs": TEST_EPOCHS,
                "monitorFrequency" : 10
            },
          },
          "validationStrategy": {
            "validSetSize": 0
          },
          "molset": self.molset.id
        }
        if initial:
            post_data["parent"] = initial.id
        response = self.client.post(create_url, data=post_data, format='json')
        self.assertEqual(response.status_code, 201)
        print(json.dumps(response.data, indent=4))

        instance = DrugExNet.objects.get(pk=response.data["id"])
        builder_class = getattr(builders, builders.DrugExNetBuilder.__name__)
        builder = builder_class(
            instance,
            initial=initial
        )
        builder.build()

        return instance

    def createAgent(self, url, exploit_net, explore_net, environ):
        post_data = {
            "name": "Test DrugEx Agent",
            "description": "test description",
            "project": self.project.id,
            "trainingStrategy": {
                "algorithm": Algorithm.objects.get(name="DrugExAgent").id,
                "mode": AlgorithmMode.objects.get(name="generator").id,
                "parameters": {
                    "nEpochs": TEST_EPOCHS,
                    "pg_batch_size" : 512,
                    "pg_mc" : 1,
                    "pg_epsilon" : 0.01,
                    "pg_beta" : 0.1,
                },
            },
            "environment": environ.id,
            "exploitationNet" : exploit_net.id,
            "explorationNet" : explore_net.id,
        }
        response = self.client.post(url, data=post_data, format='json')
        self.assertEqual(response.status_code, 201)
        print(json.dumps(response.data, indent=4))

        instance = DrugExAgent.objects.get(pk=response.data["id"])
        builder_class = getattr(builders, builders.DrugExAgentBuilder.__name__)
        builder = builder_class(
            instance
        )
        builder.build()

        return instance

    def postFile(self, instance, data):
        url = reverse('drugex-net-model-files-list', args=[instance.id])
        response = self.client.post(
            url,
            data=data,
            format='multipart'
        )
        print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, 201)

    def getBuilder(self, instance : Model, builder_module):
        builder_class = getattr(builder_module, instance.builder.name)
        return builder_class(
            instance
        )

class DrugExFromFileTestCase(SetUpDrugExGeneratorsMixIn, APITestCase):

    def setUp(self):
        super().setUp()
        self.drugex1 = self.createGenerator(reverse("drugex_net-list"))

    def test_create_from_files(self):
        instance_first = self.drugex1
        upload_main = open(instance_first.modelFile.path, "rb")
        upload_voc = open(instance_first.files.filter(note=DrugExNet.VOC_FILE_NOTE).get().path, "rb")

        create_url = reverse('drugex_net-list')
        post_data = {
            "name": "Test DrugEx Net from File",
            "project": self.project.id,
            "build" : False,
            "trainingStrategy": {
                "algorithm": Algorithm.objects.get(name="DrugExNetwork").id,
                "mode": AlgorithmMode.objects.get(name="generator").id
            },
        }
        response = self.client.post(create_url, data=post_data, format='json')
        print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, 201)
        instance = DrugExNet.objects.get(pk=response.data["id"])
        self.assertFalse(instance.modelFile)

        self.postFile(instance, {
                "file" : upload_main,
                "kind": ModelFile.MAIN,
        })
        self.postFile(instance, {
            "file" : upload_voc,
            "note" : DrugExNet.VOC_FILE_NOTE
        })

        builder = self.getBuilder(instance, builders)
        model = builder.model
        self.assertRaises(NotImplementedError, builder.build)

        mols = model.sample(100)
        self.assertTrue(len(mols) == 2)
        self.assertTrue(len(mols[0]) > 0)
        print(mols)

        response = self.client.get(reverse('generator-list'))
        self.assertEqual(response.status_code, 200)
        for generator in response.data:
            print(json.dumps(generator, indent=4))
            generator = Generator.objects.get(pk=generator["id"])
            mols = generator.get(100)
            print(mols)

class DrugExGeneratorInitTestCase(SetUpDrugExGeneratorsMixIn, APITestCase):

    def setUp(self):
        super().setUp()
        self.drugex1 = self.createGenerator(reverse("drugex_net-list"))
        self.drugex2 = self.createGenerator(reverse("drugex_net-list"), initial=self.drugex1)
        self.environ = self.createTestModel()
        self.agent = self.createAgent(reverse("drugex_agent-list"), self.drugex1, self.drugex2, self.environ)

    def test_performance_endpoints(self):
        self.assertTrue(self.drugex2.parent.id == self.drugex1.id)

        response = self.getPerformance(reverse("drugex_net_perf_view", args=[self.drugex1.id]))
        self.assertTrue(response.data["count"] > 0)

        response = self.getPerformance(reverse("drugex_agent_perf_view", args=[self.agent.id]))
        self.assertTrue(response.data["count"] > 0)

        response = self.client.get(reverse('generator-list'))
        self.assertEqual(response.status_code, 200)
        print(json.dumps(response.data, indent=4))

        path = self.agent.modelFile.path
        self.project.delete()
        self.assertFalse(os.path.exists(path))
        self.assertFalse(self.drugex2.modelFile)
        self.assertFalse(self.agent.modelFile)

    def test_generate_molset(self):
        response = self.client.get(reverse('generator-list'))
        self.assertEqual(response.status_code, 200)
        print(json.dumps(response.data, indent=4))
        generator = Generator.objects.get(pk=response.data[0]["id"])
        post_data = {
            "source" : generator.id,
            "name" : "Test Generated DrugEx Set",
            "project" : self.project.id,
            "nSamples" : 100,
        }
        response = self.client.post(reverse('generatedSet-list'), data=post_data, format='json')
        self.assertEqual(response.status_code, 201)
        print(json.dumps(response.data, indent=4))

        response = self.client.get(reverse('molset-list'))
        self.assertEqual(response.status_code, 200)
        print(json.dumps(response.data, indent=4))

        self.assertTrue(len(response.data) == 2)
        generated_set = GeneratedMolSet.objects.get(pk=response.data[1]["id"])

        initializer = getattr(initializers, "GeneratedSetInitializer")(generated_set, **{"n_samples" : post_data["nSamples"]})
        initializer.populateInstance()

        mols_url = reverse('moleculesInSet', args=[generated_set.id])
        response = self.client.get(mols_url)
        self.assertEqual(response.status_code, 200)
        print(json.dumps(response.data, indent=4))

class UseDefaultNetTestCase(SetUpDrugExGeneratorsMixIn, APITestCase):

    def setUp(self):
        super().setUp()
        self.environ = self.createTestModel()

    def test_train_exploration_net(self):
        parent = self.project.model_set.get(name__contains='ZINC')
        explore_net = self.createGenerator(reverse("drugex_net-list"), initial=parent)
        self.createAgent(reverse("drugex_agent-list"), exploit_net=parent, explore_net=explore_net, environ=self.environ)