from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch
from myapi import models as townhall_models
from django.contrib.auth.hashers import make_password

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
            is_active=True,
            password=make_password("JamesBond123"),
        )
        townhall_models.Volunteer.objects.create(
            id=11,
            first_name="Iron",
            last_name="Man",
            gender="M",
            email="ironman@yahoo.com",
            is_active=True,
            password=make_password("TonyStarkRules456"),
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

    def test_get_all_volunteers_no_filter_success(self):
        # Arrange
        self.url = "/volunteer/"
        filter_data = {"should_filter": False}

        # Act
        response = self.client.get(self.url, filter_data, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"], "All Volunteers retreived successfully"
        )
        volunteers = response.data["data"]
        self.assertEqual(len(volunteers), 2)

    def test_get_all_volunteers_one_filter_success(self):
        # Arrange
        self.url = "/volunteer/"
        filter_data = {"should_filter": True, "first_name": "Jame"}

        # Act
        response = self.client.get(self.url, filter_data, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"], "All Volunteers retreived successfully"
        )
        volunteers = response.data["data"]
        self.assertEqual(len(volunteers), 1)

    def test_get_all_volunteers_all_filters_success(self):
        # Arrange
        self.url = "/volunteer/"
        filter_data = {
            "should_filter": True,
            "first_name": "mes",
            "last_name": "Bond",
            "gender": "M",
            "email": "jamesbond@gmail.ca",
            "is_active": True,
        }

        # Act
        response = self.client.get(self.url, filter_data, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"], "All Volunteers retreived successfully"
        )
        volunteers = response.data["data"]
        self.assertEqual(len(volunteers), 1)

    def test_get_all_volunteers_optional_filters_invalid_data(self):
        # Arrange
        self.url = "/volunteer/"
        invalid_data = {
            "should_filter": True
            # Invalid becuase no filter param with should_filter=True
        }

        # Act
        response = self.client.get(self.url, invalid_data, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("myapi.services.VolunteerServices.get_all_volunteers_optional_filter")
    def test_get_all_volunteers_no_filter_success_none(
        self, mock_get_all_volunteers_optional_filter
    ):
        # Arrange
        mock_get_all_volunteers_optional_filter.return_value = (
            townhall_models.Volunteer.objects.none()
        )
        self.url = "/volunteer/"
        filter_data = {"should_filter": False}

        # Act
        response = self.client.get(self.url, filter_data, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "No Volunteers were found")

    @patch("myapi.services.VolunteerServices.get_all_volunteers_optional_filter")
    def test_get_all_volunteers_with_filter_success_none(
        self, mock_get_all_volunteers_optional_filter
    ):
        # Arrange
        mock_get_all_volunteers_optional_filter.return_value = (
            townhall_models.Volunteer.objects.none()
        )
        self.url = "/volunteer/"
        filter_data = {"should_filter": True, "is_active": False}

        # Act
        response = self.client.get(self.url, filter_data, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "No Volunteers were found")

    def test_get_all_filtered_opportunities_of_a_volunteer_no_filters(self):
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
        filter_data = {}

        # Act
        response = self.client.get(self.url, filter_data, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"],
            "Filtered Opportunities of this Volunteer retreived successfully",
        )
        opportunities = response.data["data"]
        self.assertEqual(len(opportunities), 2)

    def test_get_all_filtered_opportunities_of_a_volunteer_one_filter(self):
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
        filter_data = {
            "organization_id": 1,
        }

        # Act
        response = self.client.get(self.url, filter_data, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"],
            "Filtered Opportunities of this Volunteer retreived successfully",
        )
        opportunities = response.data["data"]
        self.assertEqual(len(opportunities), 2)

    def test_get_all_filtered_opportunities_of_a_volunteer_all_filters(self):
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
        filter_data = {
            "title": "nity2",
            "starting_start_time": "2024-07-19T21:45:00Z",
            "starting_end_time": "2024-07-21T21:45:00Z",
            "ending_start_time": "2024-07-19T21:45:00Z",
            "ending_end_time": "2024-07-21T21:45:00Z",
            "location": "le loca",
            "organization_id": 1,
        }

        # Act
        response = self.client.get(self.url, filter_data, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"],
            "Filtered Opportunities of this Volunteer retreived successfully",
        )
        opportunities = response.data["data"]
        self.assertEqual(len(opportunities), 1)

    @patch(
        "myapi.services.VolunteerServices.get_all_filtered_opportunities_of_a_volunteer"
    )
    def test_get_all_filtered_opportunities_of_a_volunteer_success_none(
        self, mock_get_all_filtered_opportunities_of_a_volunteer
    ):
        # Arrange
        empty_queryset = townhall_models.Opportunity.objects.none()
        mock_get_all_filtered_opportunities_of_a_volunteer.return_value = empty_queryset
        self.url = "/volunteer/999/opportunity/"
        filter_data = {"location": "Vancou"}

        # Act
        response = self.client.get(self.url, filter_data, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"],
            "No Opportunities were found with the specified filters",
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
        self.url = "/volunteer/1/opportunity/1/"

        # Act
        response = self.client.post(self.url, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["message"], "Volunteer Added to Opportunity Successfully"
        )
        volunteer = townhall_models.Volunteer.objects.get(id=1)
        opportunity = townhall_models.Opportunity.objects.get(id=1)
        self.assertEqual(len(volunteer.opportunities.all()), 1)
        self.assertEqual(len(opportunity.volunteers.all()), 1)

    @patch("myapi.services.VolunteerServices.add_volunteer_to_opportunity")
    def test_add_volunteer_to_opportunity_fail_service_error(
        self, mock_add_volunteer_to_opportunity
    ):
        # Arrange
        mock_add_volunteer_to_opportunity.side_effect = ValidationError(
            "random message"
        )
        self.url = "/volunteer/1/opportunity/1/"

        # Act
        response = self.client.post(self.url, format="json")

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

    def test_remove_opportunity_from_a_volunteer_success(self):
        # Pre Arrange
        test_organization = townhall_models.Organization.objects.create(
            id=1,
            name="Goodwill",
            location="Victoria",
            email="goodwill@gmail.com",
            phone_number="778-123-4567",
            website="goodwill.ca",
        )
        test_volunteer = townhall_models.Volunteer.objects.get(id=10)
        test_opportunity = townhall_models.Opportunity.objects.create(
            id=1,
            title="Food bank",
            description="Deliver food",
            start_time=timezone.make_aware(datetime(2024, 7, 20, 10, 0)),
            end_time=timezone.make_aware(datetime(2024, 7, 20, 20, 30)),
            location="Vancouver",
            organization=test_organization,
        )
        test_opportunity.volunteers.add(test_volunteer)
        test_opportunity.save()

        # Arrange
        self.url = "/volunteer/10/opportunity/1/"

        # Act
        response = self.client.delete(self.url, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"], "Opportunity removed from Volunteer successfully"
        )
        opportunities_list = list(test_volunteer.opportunities.all())
        self.assertNotIn(test_opportunity, opportunities_list)

    @patch("myapi.services.VolunteerServices.remove_volunteer_from_opportunity")
    def test_remove_opportunity_from_a_volunteer_fail_service_error(
        self, mock_remove_volunteer_from_opportunity
    ):
        # Arrange
        self.url = "/volunteer/10/opportunity/1/"
        mock_remove_volunteer_from_opportunity.side_effect = ValidationError(
            "random message"
        )

        # Act
        response = self.client.delete(self.url, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "['random message']")

    def test_update_volunteer_all_fields_success(self):
        # Arrange
        self.url = "/volunteer/10/"
        valid_data = {
            "id": 10,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "gender": "F",
            "is_active": False,
        }

        # Act
        response = self.client.patch(self.url, valid_data, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Volunteer Updated Successfully")

    def test_update_volunteer_one_field_success(self):
        # Arrange
        self.url = "/volunteer/10/"
        valid_data = {
            "id": 10,
            "email": "john.doe@example.com",
        }

        # Act
        response = self.client.patch(self.url, valid_data, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Volunteer Updated Successfully")

    def test_update_volunteer_no_fields_fail(self):
        # Arrange
        self.url = "/volunteer/10/"
        invalid_data = {
            "id": 10,
            # No Parameters to Update
        }

        # Act
        response = self.client.patch(self.url, invalid_data, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"][0], "Atleast 1 field must have a Value"
        )

    @patch("myapi.services.VolunteerServices.update_volunteer")
    def test_update_volunteer_service_error_fail(self, mock_update_volunteer):
        # Arrange
        self.url = "/volunteer/10/"
        mock_update_volunteer.side_effect = ValidationError("random message")
        valid_data = {
            "id": 10,
            "email": "john.doe@example.com",
        }

        # Act
        response = self.client.patch(self.url, valid_data, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "['random message']")

    def test_change_volunteer_password_success(self):
        # Arrange
        self.url = "/volunteer/10/change_password/"
        valid_data = {
            "id": 10,
            "email": "jamesbond@gmail.ca",
            "curr_password": "JamesBond123",
            "new_password": "IamJamesBond9",
        }

        # Act
        response = self.client.patch(self.url, valid_data, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"], "Volunteers Password Changed Successfully"
        )

    def test_change_volunteer_password_invalid_data_fail(self):
        # Arrange
        self.url = "/volunteer/10/change_password/"
        invalid_data = {
            "id": 10,
            "email": "jamesbond@gmail.ca",
            # No current Password given
            "new_password": make_password("IamJamesBond9"),
        }

        # Act
        response = self.client.patch(self.url, invalid_data, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("myapi.services.VolunteerServices.change_volunteers_password")
    def test_change_volunteer_password_service_error_fail(
        self, mock_change_volunteers_password
    ):
        # Arrange
        self.url = "/volunteer/10/change_password/"
        mock_change_volunteers_password.side_effect = ValidationError("random message")
        valid_data = {
            "id": 10,
            "email": "jamesbond@gmail.ca",
            "curr_password": make_password("JamesBond123"),
            "new_password": make_password("IamJamesBond9"),
        }

        # Act
        response = self.client.patch(self.url, valid_data, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "['random message']")
