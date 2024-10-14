from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch

from django.core.exceptions import ValidationError


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
        invalid_data = {
            "first_name": "John",
            # Invalid Data because missing email
            "email": "john.doe@example.com",
            "password": "ILikePizza9000",
            "gender": "M",
        }

        # Act
        response = self.client.post(self.url, invalid_data, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("myapi.services.VolunteerServices.create_volunteer")
    def test_create_volunteer_fail_service_error(self, mock_create_volunteer):
        # Arrange
        mock_create_volunteer.side_effect = ValidationError("random message")
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
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "['random message']")
