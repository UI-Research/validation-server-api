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

    def test_get_request_returns_runs_owned_only(self):
        self.client.force_authenticate(self.run_data[0].researcher_id)
        # get API response
        response = self.client.get(self.url)
        # get data from DB
        runs = Run.objects.filter(researcher_id=self.run_data[0].researcher_id).order_by('-run_id')
        serializer = RunSerializer(runs, many=True)
        eq_(response.data['results'], serializer.data, 'response_data:{0} \n {1}'.format(response.data, serializer.data))
        eq_(response.status_code, status.HTTP_200_OK)


class TestRunDetailTestCase(APITestCase):
    """
    Tests /api/v1/run detail operations
    """
    def setUp(self):
        self.run_data = RunFactory.create_batch(4)
        self.url = reverse('WebApp:run-detail', kwargs={'pk': self.run_data[1].pk})

    def test_get_request_for_run_not_owned_returns_forbidden(self):
        self.client.force_authenticate(self.run_data[0].researcher_id)
        # get API response
        response = self.client.get(self.url)
        eq_(response.status_code, status.HTTP_403_FORBIDDEN)

class TestBudgetDetailTestCase(APITestCase):
    """
    Tests /api/v1/budget detail operations
    """
    def setUp(self):
        self.user = UserFactory()
        self.user.is_superuser = True
        self.url = reverse('WebApp:budget-detail', kwargs={'pk': self.user.pk})
        #self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        self.client.force_authenticate(user = self.user, token = self.user.auth_token)

    def test_put_request_updates_budget(self):
        payload = {'total_budget_allocated': '100.00', 'budget_used': '25.00'}
        response = self.client.put(self.url, payload)
        eq_(response.status_code, status.HTTP_200_OK)
        eq_(response.data["total_budget_used"], "25.00")

    def test_put_request_validates_budget(self):
        payload = {'total_budget_allocated': '100.00', 'budget_used': '250.00'}
        response = self.client.put(self.url, payload)
        eq_(response.status_code, status.HTTP_400_BAD_REQUEST)