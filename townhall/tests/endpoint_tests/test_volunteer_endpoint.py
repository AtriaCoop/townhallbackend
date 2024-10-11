from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class TestEndpointVolunteer(TestCase):

    def setup(self):
        self.client = APIClient()

    # POST Volunteer
    def test_create_volunteer_success(self):
        # Arrange
        self.url = "/volunteer/create_volunteer/"
        valid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "ILikePizza9000",
            "gender": "M",
        }

        # Act
        response = self.client.post(self.url, valid_data, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Volunteer Created Successfully")

    def test_create_volunteer_fail_invalid_data(self):
        # Arrange
        self.url = "/volunteer/create_volunteer/"
        valid_data = {
            "first_name": "John",
            # Invalid Data because missing email
            "email": "john.doe@example.com",
            "password": "ILikePizza9000",
            "gender": "M",
        }

        # Act
        response = self.client.post(self.url, valid_data, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
