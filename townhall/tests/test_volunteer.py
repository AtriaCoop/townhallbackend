from django.test import TestCase
from django.core.management import call_command
from unittest.mock import patch
from django.urls import reverse
from rest_framework import status
from myapi import models as townhall_models

# VOLUNTEER

# Testing ALL tests "python manage.py test myapi.tests"
# Testing ONLY volunteer "python manage.py test myapi.tests.test_volunteer"

@patch('myapi.services.VolunteerServices')
class TestVolunteerModel(TestCase):
    fixtures = ['volunteer_fixture.json']

    def setUp(self):
        # Load the fixture data to set up initial state
        call_command('loaddata', 'volunteer_fixture.json')
        
    def test_get_volunteer(self, MockVolunteerServices):
        # Arrange: Set up the mock return value for the get_volunteer method
        mock_volunteer = townhall_models.Volunteer(
            id=1, first_name="Zamorak", last_name="Red", email="zamorak.red@gmail.com", gender="M"
        )
        MockVolunteerServices.get_volunteer.return_value = mock_volunteer

        # Act: Call the get_volunteer method with a specific ID
        volunteer_1 = MockVolunteerServices.get_volunteer(id=1)

        # Assert: Verify the returned volunteer has the expected attributes
        assert volunteer_1.first_name == "Zamorak"
        assert volunteer_1.last_name == "Red"
        assert volunteer_1.email == "zamorak.red@gmail.com"
        assert volunteer_1.gender == "M"
        # Assert: Ensure the get_volunteer method was called exactly once with the correct ID
        MockVolunteerServices.get_volunteer.assert_called_once_with(id=1)

    def test_update_volunteer(self, MockVolunteerServices):
         # Arrange: Set up the mock return value before the update
        mock_volunteer_before_update = townhall_models.Volunteer(
            id=2, first_name="Guthix", last_name="Green", email="guthix_green@hotmail.ca", gender="F"
        )
        MockVolunteerServices.get_volunteer.return_value = mock_volunteer_before_update

        # Arrange: Prepare the data for the update operation
        update_volunteer_data = townhall_models.Volunteer(
            id=2,
            first_name="Saradomin",
            last_name="Blue",
            email="saradomin.blue@gmail.com",
            gender="M"
        )
        MockVolunteerServices.update_volunteer.return_value = None

        # Act: Perform the update operation and then retrieve the updated volunteer
        volunteer_before_update = MockVolunteerServices.get_volunteer(id=2)
        MockVolunteerServices.update_volunteer(update_volunteer_data)

        # Mock the volunteer after update
        MockVolunteerServices.get_volunteer.return_value = townhall_models.Volunteer(
            id=2, first_name="Saradomin", last_name="Blue", email="saradomin.blue@gmail.com", gender="M"
        )
        updated_volunteer = MockVolunteerServices.get_volunteer(id=2)

        # Assert: Check that the initial volunteer's details were as expected
        assert volunteer_before_update.first_name == "Guthix"
        assert volunteer_before_update.last_name == "Green"
        assert volunteer_before_update.email == "guthix_green@hotmail.ca"
        assert volunteer_before_update.gender == "F"
        MockVolunteerServices.get_volunteer.assert_called_with(id=2)

        # Assert: Verify that the update operation was called with the correct data
        MockVolunteerServices.update_volunteer.assert_called_once_with(update_volunteer_data)

        # Assert: Verify the volunteer's details were updated correctly
        assert updated_volunteer.first_name == "Saradomin"
        assert updated_volunteer.last_name == "Blue"
        assert updated_volunteer.email == "saradomin.blue@gmail.com"
        assert updated_volunteer.gender == "M"

    def test_delete_volunteer(self, MockVolunteerServices):
        # Arrange: Set up the mock return value before deletion
        mock_volunteer = townhall_models.Volunteer(
            id=1, first_name="Zamorak", last_name="Red", email="zamorak.red@gmail.com", gender="M"
        )
        MockVolunteerServices.get_volunteer.return_value = mock_volunteer

        # Act: Retrieve the volunteer and then delete it
        volunteer_1 = MockVolunteerServices.get_volunteer(id=1)
        MockVolunteerServices.delete_volunteer(id=1)
        MockVolunteerServices.get_volunteer.return_value = None

        # Act: Attempt to retrieve the volunteer after deletion
        volunteer_after_deletion = MockVolunteerServices.get_volunteer(id=1)

        # Assert: Verify the volunteer's initial details were correct
        assert volunteer_1.first_name == "Zamorak"
        assert volunteer_1.last_name == "Red"
        assert volunteer_1.email == "zamorak.red@gmail.com"
        assert volunteer_1.gender == "M"

        # Assert: Ensure the volunteer was deleted successfully
        MockVolunteerServices.get_volunteer.assert_called_once_with(id=1)

        # Assert: Check that the volunteer no longer exists after deletion
        MockVolunteerServices.delete_volunteer.assert_called_once_with(id=1)
        assert volunteer_after_deletion is None

    def test_get_all_volunteers(self, MockVolunteerServices):
        # Arrange: Mock the return value for getting all volunteers
        MockVolunteerServices.get_volunteers_all.return_value = [
            townhall_models.Volunteer(id=1, first_name="Zamorak", last_name="Red", email="zamorak.red@gmail.com", gender="M"),
            townhall_models.Volunteer(id=2, first_name="Guthix", last_name="Green", email="guthix.green@hotmail.ca", gender="F")
        ]

        # Act: Retrieve all volunteers
        volunteers = MockVolunteerServices.get_volunteers_all()

        # Assert: Verify the correct number of volunteers is returned
        assert len(volunteers) == 2
        assert volunteers[0].first_name == "Zamorak"
        assert volunteers[1].first_name == "Guthix"
        # Assert: Ensure the get_volunteers_all method was called exactly once
        MockVolunteerServices.get_volunteers_all.assert_called_once()

    def test_get_all_volunteers_empty(self, MockVolunteerServices):
        # Arrange: Mock the return value for getting all volunteers to be an empty list
        MockVolunteerServices.get_volunteers_all.return_value = []

        # Act: Retrieve all volunteers when none exist
        volunteers = MockVolunteerServices.get_volunteers_all()

        # Assert: Verify that no volunteers are returned
        assert len(volunteers) == 0
        # Assert: Ensure the get_volunteers_all method was called exactly once
        MockVolunteerServices.get_volunteers_all.assert_called_once()
        volunteers = townhall_services.VolunteerServices.get_volunteers_all()
        assert len(volunteers) == 0, "There should be no volunteers"

    def test_update_volunteer_success(self):
        # Arrange: Set up the data for a successful update
        # This is the new data that we want to update the volunteer with.
        updated_data = {
            "first_name": "Saradomin",
            "last_name": "Blue",
            "email": "saradomin.blue@gmail.com",
            "gender": "M"
        }

        # Create an instance of the APIClient, which allows us to simulate HTTP requests.
        client = APIClient()

        # Act: Perform the PUT request to update the volunteer
        response = client.put(
            reverse('update_volunteer', kwargs={'pk': 2}),
            updated_data,
            format='json',  # Indicating that the data is in JSON format
            content_type='application/json'  # Setting the content type to application/json
        )

        # Assert: Verify that the response is as expected
        assert response.status_code == status.HTTP_200_OK
        assert response.data['first_name'] == "Saradomin"
        assert response.data['last_name'] == "Blue"
        assert response.data['email'] == "saradomin.blue@gmail.com"
        assert response.data['gender'] == "M"

    def test_update_volunteer_invalid_data(self):
        # Arrange: Set up the data for an invalid update
        invalid_data = {
            "first_name": "",
            "last_name": "Blue",
            "email": "not-an-email",
            "gender": "X"
        }

        # Create an instance of the APIClient, which allows us to simulate HTTP requests.
        client = APIClient()

        # Act: Perform the PUT request with invalid data
        response = client.put(
            reverse('update_volunteer', kwargs={'pk': 2}),
            invalid_data,
            format='json',  # Indicating that the data is in JSON format
            content_type='application/json'  # Setting the content type to application/json
        )

        # Assert: Verify that the response is as expected
        assert response.status_code == status.HTTP_400_BAD_REQUEST
