from rest_framework.test import APITestCase, APIClient
from django.core.management import call_command
from rest_framework import status
from myapi.models import Volunteer, Organization, Task
from django.utils import timezone
from datetime import datetime

class TaskEndpointTests(APITestCase):

    @classmethod
    def setUpClass(cls):
        """
        Load fixtures and set up test data before running tests.
        """
        super().setUpClass()
        # Load the volunteer and organization fixtures
        call_command('loaddata', 'volunteer_fixture.json')
        call_command('loaddata', 'organization_fixture.json')
        call_command('loaddata', 'task_fixture.json')

    def setUp(self):
        """
        Set up the test environment before each test.
        """
        self.client = APIClient()
        # Get the volunteer and organization from the fixture
        self.volunteer = Volunteer.objects.get(pk=1)
        self.organization = Organization.objects.get(pk=1)
        
        # Mock task data
        self.task_data = {
            'name': 'Test Task',
            'description': 'Task description',
            'deadline': '2024-12-31T23:59:59Z',
            'status': 'open',
            'assigned_to': self.volunteer.id,
            'created_by': self.volunteer.id,
            'organization': self.organization.id
        }

        # Authenticate with a valid user (volunteer)
        self.client.force_authenticate(user=self.volunteer)

    def test_create_task(self):
        """
        Test the creation of a task.
        """
        # Arrange: Define the URL for task creation
        url = '/tasks/'

        # Act: Make a POST request to create a task
        response = self.client.post(url, self.task_data, format='json')

        # Assert: Ensure the response is successful and task is created with expected values
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_task(self):
        """
        Test retrieving a specific task by ID.
        """
        # Arrange: Create a task and get its ID
        create_response = self.client.post('/tasks/', self.task_data, format='json')
        task_id = create_response.data['id']
        url = f'/tasks/{task_id}/'

        # Act: Make a GET request to retrieve the task
        response = self.client.get(url)

        # Assert: Ensure the response is successful and task data is as expected
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Task')

    def test_update_task(self):
        """
        Test updating a specific task by ID.
        """
        # Arrange: Create a task and prepare new data to update the task
        create_response = self.client.post('/tasks/', self.task_data, format='json')
        task_id = create_response.data['id']
        url = f'/tasks/{task_id}/'
        update_data = {'name': 'Updated Task'}

        # Act: Make a PUT request to update the task
        response = self.client.put(url, update_data, format='json')

        # Assert: Ensure the response is successful and task is updated correctly
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Task')

    def test_delete_task(self):
        """
        Test deleting a task by ID.
        """
        # Arrange: Create a task and get its ID
        create_response = self.client.post('/tasks/', self.task_data, format='json')
        task_id = create_response.data['id']
        url = f'/tasks/{task_id}/'

        # Act: Make a DELETE request to remove the task
        response = self.client.delete(url)

        # Assert: Ensure the response is successful and the task is deleted
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Act: Try to get the deleted task to ensure it no longer exists
        get_response = self.client.get(url)

        # Assert: Ensure the task no longer exists
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)
