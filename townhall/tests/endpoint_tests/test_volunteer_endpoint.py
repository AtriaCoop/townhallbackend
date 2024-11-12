from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch
from myapi import models as townhall_models

from datetime import datetime
from django.utils import timezone

from django.core.exceptions import ValidationError


class TestEndpointVolunteer(TestCase):

    def setUp(self):
        self.client = APIClient()
        townhall_models.Volunteer.objects.create(
            id=10,
            first_name="James",
            last_name="Bond",
            gender="M",
            email="jamesbond@gmail.ca",
        )
        townhall_models.Volunteer.objects.create(
            id=11,
            first_name="Iron",
            last_name="Man",
            gender="M",
            email="ironman@yahoo.com",
        )

    def test_get_volunteer_success(self):
        # Arrange
        self.url = "/volunteer/10/"

        # Act
        response = self.client.get(self.url, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Volunteer Retreived Successfully")
        self.assertEqual(response.data["volunteer"]["first_name"], "James")
        self.assertEqual(response.data["volunteer"]["last_name"], "Bond")
        self.assertEqual(response.data["volunteer"]["email"], "jamesbond@gmail.ca")
        self.assertEqual(response.data["volunteer"]["gender"], "M")
        self.assertEqual(response.data["volunteer"]["is_active"], True)

    def test_get_volunteer_fail_service_error(self):
        # Arrange
        self.url = "/volunteer/999/"

        # Act
        response = self.client.get(self.url, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["message"],
            "['Volunteer with the given id: 999, does not exist.']",
        )

    def test_get_all_volunteers_success(self):
        # Arrange
        self.url = "/volunteer/"

        # Act
        response = self.client.get(self.url, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"], "All Volunteers retreived successfully"
        )
        volunteers = response.data["data"]
        self.assertEqual(len(volunteers), 2)

    @patch("myapi.services.VolunteerServices.get_volunteers_all")
    def test_get_all_volunteers_success_none(self, mock_get_volunteers_all):
        # Arrange
        mock_get_volunteers_all.return_value = townhall_models.Volunteer.objects.none()
        self.url = "/volunteer/"

        # Act
        response = self.client.get(self.url, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "No Volunteers were found")

    def test_get_all_opportunities_of_a_volunteer_success(self):
        # Arrange
        organization = townhall_models.Organization.objects.create(
            id=1,
            name="Sample Organization",
            location="Sample Location",
            email="Sample Email",
            phone_number="Sample Phone Number",
            website="Sample Website",
        )
        opportunity1 = townhall_models.Opportunity.objects.create(
            id=1,
            title="Sample Opportunity1",
            start_time=timezone.make_aware(datetime(2024, 7, 20, 10, 0)),
            end_time=timezone.make_aware(datetime(2024, 7, 20, 10, 0)),
            description="Sample description",
            location="Sample location",
            organization=organization,
        )
        opportunity2 = townhall_models.Opportunity.objects.create(
            id=2,
            title="Sample Opportunity2",
            start_time=timezone.make_aware(datetime(2024, 7, 20, 10, 0)),
            end_time=timezone.make_aware(datetime(2024, 7, 20, 10, 0)),
            description="Sample description",
            location="Sample location",
            organization=organization,
        )
        opportunity1.volunteers.add(townhall_models.Volunteer.objects.get(id=10))
        opportunity2.volunteers.add(townhall_models.Volunteer.objects.get(id=10))
        self.url = "/volunteer/10/opportunity/"

        # Act
        response = self.client.get(self.url, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"],
            "Opportunities of this Volunteer retreived successfully",
        )
        volunteers = response.data["data"]
        self.assertEqual(len(volunteers), 2)

    @patch("myapi.services.VolunteerServices.get_all_opportunities_of_a_volunteer")
    def test_get_all_opportunities_of_a_volunteer_success_none(
        self, mock_get_all_opportunities_of_a_volunteer
    ):
        # Arrange
        empty_queryset = townhall_models.Opportunity.objects.none()
        mock_get_all_opportunities_of_a_volunteer.return_value = empty_queryset
        self.url = "/volunteer/11/opportunity/"

        # Act
        response = self.client.get(self.url, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "No Opportunities were found")

    def test_get_all_opportunities_of_a_volunteer_fail_service_error(self):
        # Arrange
        self.url = "/volunteer/999/opportunity/"

        # Act
        response = self.client.get(self.url, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["message"],
            "['Volunteer with the given id: 999, does not exist.']",
        )

    def test_create_volunteer_success(self):
        # Arrange
        self.url = "/volunteer/"
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
        self.url = "/volunteer/"
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
        self.url = "/volunteer/"
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

    def test_add_volunteer_to_opportunity_success(self):
        # Pre Arrange
        townhall_models.Organization.objects.create(
            id=1,
            name="Goodwill",
            location="Victoria",
            email="goodwill@gmail.com",
            phone_number="778-123-4567",
            website="goodwill.ca",
        )
        test_organization = townhall_models.Organization.objects.get(id=1)
        townhall_models.Opportunity.objects.create(
            id=1,
            title="Food bank",
            description="Deliver food",
            start_time=timezone.make_aware(datetime(2024, 7, 20, 10, 0)),
            end_time=timezone.make_aware(datetime(2024, 7, 20, 20, 30)),
            location="Vancouver",
            organization=test_organization,
        )
        townhall_models.Volunteer.objects.create(
            id=1,
            first_name="Zamorak",
            last_name="Red",
            gender="M",
            email="zamorak.red@gmail.com",
        )

        # Arrange
        self.url = "/volunteer/1/opportunity/"
        valid_data = {"opportunity_id": 1}

        # Act
        response = self.client.post(self.url, valid_data, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["message"], "Volunteer Added to Opportunity Successfully"
        )
        volunteer = townhall_models.Volunteer.objects.get(id=1)
        opportunity = townhall_models.Opportunity.objects.get(id=1)
        self.assertEqual(len(volunteer.opportunities.all()), 1)
        self.assertEqual(len(opportunity.volunteers.all()), 1)

    def test_add_volunteer_to_opportunity_fail_invalid_data(self):
        # Arrange
        self.url = "/volunteer/1/opportunity/"
        invalid_data = {"opportunity_id": "one"}

        # Act
        response = self.client.post(self.url, invalid_data, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("myapi.services.VolunteerServices.add_volunteer_to_opportunity")
    def test_add_volunteer_to_opportunity_fail_service_error(
        self, mock_add_volunteer_to_opportunity
    ):
        # Arrange
        mock_add_volunteer_to_opportunity.side_effect = ValidationError(
            "random message"
        )
        self.url = "/volunteer/1/opportunity/"
        valid_data = {"opportunity_id": 1}

        # Act
        response = self.client.post(self.url, valid_data, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "['random message']")

    def test_delete_volunteer_success(self):
        # Arrange
        self.url = "/volunteer/10/"

        # Act
        response = self.client.delete(self.url, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Volunteer Deleted Successfully")
        try:
            townhall_models.Volunteer.objects.get(id=10)
            self.fail("Should have returned a Volunteer Does Not Exist Error")
        except townhall_models.Volunteer.DoesNotExist:
            pass

    def test_delete_volunteer_fail_does_not_exist(self):
        # Arrange
        self.url = "/volunteer/999/"  # Assuming ID 999 doesn't exist

        # Act
        response = self.client.delete(self.url, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["message"],
            "['Volunteer with the given id: 999, does not exist.']",
        )
