from django.test import TestCase
from django.core.management import call_command
from unittest.mock import patch, MagicMock
from django.core.exceptions import ValidationError
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
        MockVolunteerServices.get_volunteer.side_effect = [mock_volunteer, None]

        # Act: Retrieve the volunteer and then delete it
        volunteer_1 = MockVolunteerServices.get_volunteer(id=1)
        MockVolunteerServices.delete_volunteer(id=1)
        volunteer_after_deletion = MockVolunteerServices.get_volunteer(id=1)

        # Assert: Verify the volunteer's initial details were correct
        assert volunteer_1.first_name == "Zamorak"
        assert volunteer_1.last_name == "Red"
        assert volunteer_1.email == "zamorak.red@gmail.com"
        assert volunteer_1.gender == "M"

        # Assert: Ensure the volunteer was deleted successfully
        MockVolunteerServices.get_volunteer.assert_called_with(id=1)
        MockVolunteerServices.get_volunteer.assert_called_with(id=1)
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

    def test_update_volunteer_success(self, MockVolunteerServices):
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
        MockVolunteerServices.update_volunteer(update_volunteer_data)

        # Arrange: Mock the return value after the update
        MockVolunteerServices.get_volunteer.return_value = townhall_models.Volunteer(
            id=2, first_name="Saradomin", last_name="Blue", email="saradomin.blue@gmail.com", gender="M"
        )
        updated_volunteer = MockVolunteerServices.get_volunteer(id=2)

        # Assert: Verify that the update operation was called with the correct data
        MockVolunteerServices.update_volunteer.assert_called_once_with(update_volunteer_data)
        assert updated_volunteer.first_name == "Saradomin"
        assert updated_volunteer.last_name == "Blue"
        assert updated_volunteer.email == "saradomin.blue@gmail.com"
        assert updated_volunteer.gender == "M"

    def test_update_volunteer_invalid_data(self, MockVolunteerServices):
        # Arrange: Mock the return value for the get_volunteer method
        mock_volunteer_before_update = townhall_models.Volunteer(
            id=2, first_name="Guthix", last_name="Green", email="guthix_green@hotmail.ca", gender="F"
        )
        MockVolunteerServices.get_volunteer.return_value = mock_volunteer_before_update

        # Arrange: Prepare invalid update data
        invalid_data = townhall_models.Volunteer(
            id=2,
            first_name="",
            last_name="Blue",
            email="not-an-email",
            gender="X"
        )

        # Act: Attempt to update the volunteer with invalid data
        MockVolunteerServices.update_volunteer(invalid_data)

        # Assert: Ensure the update operation was attempted with invalid data
        MockVolunteerServices.update_volunteer.assert_called_once_with(invalid_data)

    def test_authenticate_volunteer_success(self, MockVolunteerServices):
        # Arrange: Mock successful authentication
        mock_volunteer = townhall_models.Volunteer(
            id=1, first_name="Zamorak", last_name="Red", email="zamorak.red@gmail.com", gender="M"
        )
        MockVolunteerServices.authenticate_volunteer.return_value = mock_volunteer

        # Act: Authenticate with correct credentials
        volunteer = MockVolunteerServices.authenticate_volunteer(username="zamorak", password="correct_password")

        # Assert: Check that the returned volunteer is as expected
        assert volunteer is not None
        assert volunteer.first_name == "Zamorak"
        assert volunteer.last_name == "Red"
        MockVolunteerServices.authenticate_volunteer.assert_called_once_with(username="zamorak", password="correct_password")

    def test_authenticate_volunteer_failure(self, MockVolunteerServices):
        # Arrange: Mock failed authentication
        MockVolunteerServices.authenticate_volunteer.return_value = None

        # Act: Attempt to authenticate with incorrect credentials
        volunteer = MockVolunteerServices.authenticate_volunteer(username="zamorak", password="wrong_password")

        # Assert: Ensure that the authentication fails and returns None
        assert volunteer is None
        MockVolunteerServices.authenticate_volunteer.assert_called_once_with(username="zamorak", password="wrong_password")

    def test_validate_username_and_password_success(self, MockVolunteerServices):
        # Arrange: No setup needed for successful validation
        MockVolunteerServices.validate_username_and_password.return_value = None

        # Act: Validate correct username and password
        MockVolunteerServices.validate_username_and_password(username="zamorak", password="StrongPassword123!")

        # Assert: Ensure that validation was called with correct arguments
        MockVolunteerServices.validate_username_and_password.assert_called_once_with(username="zamorak", password="StrongPassword123!")

    def test_validate_username_and_password_failure(self, MockVolunteerServices):
        # Arrange: Mock validation failure
        MockVolunteerServices.validate_username_and_password.side_effect = ValidationError("Invalid password")

        # Act & Assert: Attempt validation and expect a ValidationError
        with self.assertRaises(ValidationError):
            MockVolunteerServices.validate_username_and_password(username="zamorak", password="weakpass")

        MockVolunteerServices.validate_username_and_password.assert_called_once_with(username="zamorak", password="weakpass")

    def test_encrypt_password_success(self, MockVolunteerServices):
        # Arrange: Mock the password encryption
        MockVolunteerServices.encrypt_password.return_value = "encrypted_password"

        # Act: Encrypt a valid password
        encrypted_password = MockVolunteerServices.encrypt_password("StrongPassword123!")

        # Assert: Ensure the encryption method was called correctly
        assert encrypted_password == "encrypted_password"
        MockVolunteerServices.encrypt_password.assert_called_once_with("StrongPassword123!")

    def test_change_password_success(self, MockVolunteerServices):
        # Arrange: Mock the successful password change
        MockVolunteerServices.change_password.return_value = None

        # Act: Change the password for a volunteer
        MockVolunteerServices.change_password(volunteer_id=1, old_password="OldPassword123!", new_password="NewPassword456!")

        # Assert: Ensure the change password method was called with correct arguments
        MockVolunteerServices.change_password.assert_called_once_with(volunteer_id=1, old_password="OldPassword123!", new_password="NewPassword456!")

    def test_change_password_failure_due_to_old_password(self, MockVolunteerServices):
        # Arrange: Mock failure due to incorrect old password
        MockVolunteerServices.change_password.side_effect = ValidationError("Old password is incorrect")

        # Act & Assert: Attempt to change password and expect a ValidationError
        with self.assertRaises(ValidationError):
            MockVolunteerServices.change_password(volunteer_id=1, old_password="WrongOldPassword!", new_password="NewPassword456!")

        MockVolunteerServices.change_password.assert_called_once_with(volunteer_id=1, old_password="WrongOldPassword!", new_password="NewPassword456!")

    def test_change_password_failure_due_to_password_reuse(self, MockVolunteerServices):
        # Arrange: Mock failure due to password reuse
        MockVolunteerServices.change_password.side_effect = ValidationError("You cannot reuse a recent password")

        # Act & Assert: Attempt to change password to a recent password and expect a ValidationError
        with self.assertRaises(ValidationError):
            MockVolunteerServices.change_password(volunteer_id=1, old_password="OldPassword123!", new_password="OldPassword123!")

        MockVolunteerServices.change_password.assert_called_once_with(volunteer_id=1, old_password="OldPassword123!", new_password="OldPassword123!")
