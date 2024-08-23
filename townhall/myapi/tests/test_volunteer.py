from django.test import TestCase
from django.core.management import call_command
from unittest.mock import patch, MagicMock
from myapi import models as townhall_models

# VOLUNTEER

# Testing ALL tests "python manage.py test myapi.tests"
# Testing ONLY volunteer "python manage.py test myapi.tests.test_volunteer"

@patch('myapi.services.VolunteerServices')
class TestVolunteerModel(TestCase):
    fixtures = ['volunteer_fixture.json']

    def setUp(self):
        # Load the fixture data
        call_command('loaddata', 'volunteer_fixture.json')
        

    def test_get_volunteer(self, MockVolunteerServices):
        # Mocking the get_volunteer method
        mock_volunteer = townhall_models.Volunteer(
            id=1, first_name="Zamorak", last_name="Red", email="zamorak.red@gmail.com", gender="M"
        )
        MockVolunteerServices.get_volunteer.return_value = mock_volunteer

        volunteer_1 = MockVolunteerServices.get_volunteer(id=1)

        assert volunteer_1.first_name == "Zamorak"
        assert volunteer_1.last_name == "Red"
        assert volunteer_1.email == "zamorak.red@gmail.com"
        assert volunteer_1.gender == "M"
        MockVolunteerServices.get_volunteer.assert_called_once_with(id=1)

    def test_update_volunteer(self, MockVolunteerServices):
        # Mocking the get_volunteer method before update
        mock_volunteer_before_update = townhall_models.Volunteer(
            id=2, first_name="Guthix", last_name="Green", email="guthix_green@hotmail.ca", gender="F"
        )
        MockVolunteerServices.get_volunteer.return_value = mock_volunteer_before_update

        # Step 1: Getting the volunteer and make sure it exists
        volunteer_before_update = MockVolunteerServices.get_volunteer(id=2)
        assert volunteer_before_update.first_name == "Guthix"
        assert volunteer_before_update.last_name == "Green"
        assert volunteer_before_update.email == "guthix_green@hotmail.ca"
        assert volunteer_before_update.gender == "F"
        MockVolunteerServices.get_volunteer.assert_called_once_with(id=2)
        
        # Step 2: Update
        update_volunteer_data = townhall_models.Volunteer(
            id=2,
            first_name="Saradomin",
            last_name="Blue",
            email="saradomin.blue@gmail.com",
            gender="M"
        )
        MockVolunteerServices.update_volunteer.return_value = None
        MockVolunteerServices.update_volunteer(update_volunteer_data)

        # Assertions
        MockVolunteerServices.update_volunteer.assert_called_once_with(update_volunteer_data)

        # Step 3: Fetching volunteer and making sure the update was successful

        # Mocking the get_volunteer method after update
        MockVolunteerServices.get_volunteer.return_value = townhall_models.Volunteer(
            id=2, first_name="Saradomin", last_name="Blue", email="saradomin.blue@gmail.com", gender="M"
        )
        # Additional test : Delete step 2 and try to GET volunteer_before_update information and it should pass
        updated_volunteer = MockVolunteerServices.get_volunteer(id=2)
        assert updated_volunteer.first_name == "Saradomin"
        assert updated_volunteer.last_name == "Blue"
        assert updated_volunteer.email == "saradomin.blue@gmail.com"
        assert updated_volunteer.gender == "M"
        MockVolunteerServices.get_volunteer.assert_called_with(id=2)

    def test_delete_volunteer(self, MockVolunteerServices):
        # Mocking the get_volunteer method before delete
        mock_volunteer = townhall_models.Volunteer(
            id=1, first_name="Zamorak", last_name="Red", email="zamorak.red@gmail.com", gender="M"
        )
        MockVolunteerServices.get_volunteer.return_value = mock_volunteer

        # Step 1
        volunteer_1 = MockVolunteerServices.get_volunteer(id=1)
        assert volunteer_1.first_name == "Zamorak"
        assert volunteer_1.last_name == "Red"
        assert volunteer_1.email == "zamorak.red@gmail.com"
        assert volunteer_1.gender == "M"
        MockVolunteerServices.get_volunteer.assert_called_once_with(id=1)

        # Mocking the delete_volunteer method
        MockVolunteerServices.delete_volunteer.return_value = None
        MockVolunteerServices.delete_volunteer(id=1)
        MockVolunteerServices.delete_volunteer.assert_called_once_with(id=1)

        # Mocking the get_volunteer method after delete
        MockVolunteerServices.get_volunteer.return_value = None
        assert MockVolunteerServices.get_volunteer(id=1) is None
        MockVolunteerServices.get_volunteer.assert_called_with(id=1)

        # Retrieving all volunteers
    def test_get_all_volunteers(self, MockVolunteerServices):
        # Mocking the get_volunteers_all method
        MockVolunteerServices.get_volunteers_all.return_value = [
            townhall_models.Volunteer(id=1, first_name="Zamorak", last_name="Red", email="zamorak.red@gmail.com", gender="M"),
            townhall_models.Volunteer(id=2, first_name="Guthix", last_name="Green", email="guthix.green@hotmail.ca", gender="F")
        ]

        volunteers = MockVolunteerServices.get_volunteers_all()
        assert len(volunteers) == 2, "There should be two volunteers"
        assert volunteers[0].first_name == "Zamorak"
        assert volunteers[1].first_name == "Guthix"
        MockVolunteerServices.get_volunteers_all.assert_called_once()

    # Retrieving all volunteers when there are none
    def test_get_all_volunteers_empty(self, MockVolunteerServices):
        
        # Mocking the get_volunteers_all method for an empty result
        MockVolunteerServices.get_volunteers_all.return_value = []
        volunteers = MockVolunteerServices.get_volunteers_all()
        assert len(volunteers) == 0
        MockVolunteerServices.get_volunteers_all.assert_called_once()
