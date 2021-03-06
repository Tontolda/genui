import json
import os

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from genui.projects.tests import ProjectMixIn


class SDFMolSetTestCase(ProjectMixIn, APITestCase):

    def setUp(self):
        super().setUp()
        self.project = self.createProject()

    def test_sdf_create(self):
        post_data = {
            'file': open(os.path.join(os.path.dirname(__file__), 'test_files/init.sdf')),
            'name': "Molecule Set from an SDF",
            'project': self.project.id
        }
        url = reverse('sdfSet-list')
        response = self.client.post(url, post_data)
        print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, 201)

        # get the object detail from API
        url = reverse('sdfSet-detail', args=[response.data['id']])
        response = self.client.get(url)
        print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, 200)

        # get the activities
        url = reverse('activitySet-activities', args=[response.data['activities'][0]])
        response = self.client.get(url)
        print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['count'] > 0)
