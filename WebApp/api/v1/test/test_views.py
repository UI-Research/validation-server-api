from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from WebApp.api.v1.models import Run
from WebApp.api.v1.serializers import RunSerializer 
from WebApp.api.v1.views import RunList
from nose.tools import eq_, ok_
from WebApp.api.v1.test.factories import RunFactory
from WebApp.users.test.factories import UserFactory
from faker import Faker
import factory

fake = Faker()

class TestRunListTestCase(APITestCase):
    """ 
    Tests /api/v1/runs list operations 
    """
    def setUp(self):
        self.url = reverse('WebApp:run-list')
        self.run_data = RunFactory.create_batch(4)
        self.client.force_authenticate(self.run_data[0].researcher_id)

    def test_get_request_returns_all_runs(self):
        # get API response
        response = self.client.get(self.url)
        # get data from DB
        runs = Run.objects.all().order_by('-run_id')
        serializer = RunSerializer(runs, many=True)
        eq_(response.data['results'], serializer.data, 'response_data:{0} \n {1}'.format(response.data, serializer.data))
        eq_(response.status_code, status.HTTP_200_OK)
