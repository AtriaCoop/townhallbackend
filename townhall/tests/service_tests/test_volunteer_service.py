from django.test import TestCase
from django.core.management import call_command

from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password, make_password

from myapi import models as townhall_models
from myapi import services as townhall_services

from myapi.types import UpdateVolunteerData
from myapi.types import ChangeVolunteerPasswordData


# VOLUNTEER

# Testing ALL tests "python manage.py test myapi.tests"
# Testing ONLY volunteer "python manage.py test myapi.tests.test_volunteer"


class TestVolunteerModel(TestCase):
    def setUp(self):
        # Arrange (For all non-mock tests)
        call_command("loaddata", "volunteer_fixture.json")
        call_command("loaddata", "opportunity_fixture.json")

    def test_get_all_volunteers(self):
        # Act
        volunteers = townhall_services.VolunteerServices.get_volunteers_all()

        # Assert
        assert len(volunteers) == 2
        ids = [volunteer.id for volunteer in volunteers]
        assert set(ids) == {1, 2}

    def test_get_volunteer_found(self):
        # Act
        volunteer = townhall_services.VolunteerServices.get_volunteer(id=1)

        # Assert
        assert volunteer.first_name == "Zamorak"
        assert volunteer.last_name == "Red"
        assert volunteer.email == "zamorak.red@gmail.com"
        assert volunteer.gender == "M"
        split_string = (
            "pbkdf2_sha256$320000$eERGy7Egdf2$"
            "Rh6s7lqJXJH7dZJsZUZ7ix77E6EsHZaFL3Q8vPBvmfI="
        )
        assert volunteer.password == split_string
        assert volunteer.is_active is True

    @patch("myapi.dao.VolunteerDao.get_volunteer")
    def test_get_volunteer_failed_not_found(self, mock_get_volunteer):
        # Arrange
        mock_get_volunteer.side_effect = townhall_models.Volunteer.DoesNotExist
        volunteer_id = 999  # Assuming this ID does not exist

        # Act & Assert
        with self.assertRaises(ValidationError) as context:
            townhall_services.VolunteerServices.get_volunteer(volunteer_id)

        # Assert
        assert (
            str(context.exception)
            == f"['Volunteer with the given id: {volunteer_id}, does not exist.']"
        )

    def test_get_all_opportunities_of_volunteer_found(self):
        # Arrange
        opportunity1 = townhall_models.Opportunity.objects.get(id=1)
        opportunity2 = townhall_models.Opportunity.objects.get(id=2)
        volunteer = townhall_services.VolunteerServices.get_volunteer(id=1)
        opportunity1.volunteers.add(volunteer)
        opportunity2.volunteers.add(volunteer)

        # Act
        opportunities = (
            townhall_services.VolunteerServices.get_all_opportunities_of_a_volunteer(1)
        )

        # Assert
        assert len(opportunities) == 2
        ids = [opportunity.id for opportunity in opportunities]
        assert set(ids) == {1, 2}

    @patch("myapi.dao.VolunteerDao.get_all_opportunities_of_a_volunteer")
    def test_get_all_opportunities_of_volunteer_not_found(
        self, mock_get_all_opportunities_of_a_volunteer
    ):
        # Arrange
        mock_get_all_opportunities_of_a_volunteer.side_effect = (
            townhall_models.Volunteer.DoesNotExist
        )
        volunteer_id = 999  # Assuming this ID does not exist

        # Act & Assert
        with self.assertRaises(ValidationError) as context:
            townhall_services.VolunteerServices.get_all_opportunities_of_a_volunteer(
                volunteer_id
            )

        # Assert
        assert (
            str(context.exception)
            == f"['Volunteer with the given id: {volunteer_id}, does not exist.']"
        )

    def test_add_volunteer_to_opportunity_success(self):
        # Act
        townhall_services.VolunteerServices.add_volunteer_to_opportunity(1, 1)

        # Assert
        volunteer = townhall_services.VolunteerServices.get_volunteer(id=1)
        assert len(volunteer.opportunities.all()) == 1
        ids = [opportunity.id for opportunity in volunteer.opportunities.all()]
        assert set(ids) == {1}

    @patch("myapi.dao.VolunteerDao.add_volunteer_to_opportunity")
    def test_add_volunteer_to_opportunity_volunteer_not_found(
        self, mock_add_volunteer_to_opportunity
    ):
        # Arrange
        mock_add_volunteer_to_opportunity.side_effect = (
            townhall_models.Volunteer.DoesNotExist
        )
        volunteer_id = 999  # Assuming this ID does not exist

        # Act & Assert
        with self.assertRaises(ValidationError) as context:
            townhall_services.VolunteerServices.add_volunteer_to_opportunity(
                volunteer_id, 1
            )

        # Assert
        assert (
            str(context.exception)
            == f"['Volunteer with the given id: {volunteer_id}, does not exist.']"
        )

    @patch("myapi.dao.VolunteerDao.add_volunteer_to_opportunity")
    def test_add_volunteer_to_opportunity_opportunity_not_found(
        self, mock_add_volunteer_to_opportunity
    ):
        # Arrange
        mock_add_volunteer_to_opportunity.side_effect = (
            townhall_models.Opportunity.DoesNotExist
        )
        opportunity_id = 999  # Assuming this ID does not exist

        # Act & Assert
        with self.assertRaises(ValidationError) as context:
            townhall_services.VolunteerServices.add_volunteer_to_opportunity(
                1, opportunity_id
            )

        # Assert
        assert (
            str(context.exception)
            == f"['Opportunity with the given id: {opportunity_id}, does not exist.']"
        )

    def test_remove_volunteer_from_opportunity_success(self):
        # Arrange
        opportunity1 = townhall_models.Opportunity.objects.get(id=1)
        opportunity2 = townhall_models.Opportunity.objects.get(id=2)
        volunteer = townhall_services.VolunteerServices.get_volunteer(id=1)
        opportunity1.volunteers.add(volunteer)
        opportunity2.volunteers.add(volunteer)

        # Act
        townhall_services.VolunteerServices.remove_volunteer_from_opportunity(1, 1)

        # Assert
        volunteer = townhall_services.VolunteerServices.get_volunteer(id=1)
        assert len(volunteer.opportunities.all()) == 1
        ids = [opportunity.id for opportunity in volunteer.opportunities.all()]
        assert set(ids) == {2}

    @patch("myapi.dao.VolunteerDao.remove_volunteer_from_opportunity")
    def test_remove_volunteer_from_opportunity_volunteer_not_found(
        self, mock_remove_volunteer_from_opportunity
    ):
        # Arrange
        mock_remove_volunteer_from_opportunity.side_effect = (
            townhall_models.Volunteer.DoesNotExist
        )
        volunteer_id = 999  # Assuming this ID does not exist

        # Act & Assert
        with self.assertRaises(ValidationError) as context:
            townhall_services.VolunteerServices.remove_volunteer_from_opportunity(
                volunteer_id, 1
            )

        # Assert
        assert (
            str(context.exception)
            == f"['Volunteer with the given id: {volunteer_id}, does not exist.']"
        )

    @patch("myapi.dao.VolunteerDao.remove_volunteer_from_opportunity")
    def test_remove_volunteer_from_opportunity_opportunity_not_found(
        self, mock_remove_volunteer_from_opportunity
    ):
        # Arrange
        mock_remove_volunteer_from_opportunity.side_effect = (
            townhall_models.Opportunity.DoesNotExist
        )
        opportunity_id = 999  # Assuming this ID does not exist

        # Act & Assert
        with self.assertRaises(ValidationError) as context:
            townhall_services.VolunteerServices.add_volunteer_to_opportunity(
                1, opportunity_id
            )

        # Assert
        assert (
            str(context.exception)
            == f"['Opportunity with the given id: {opportunity_id}, does not exist.']"
        )

    def test_update_volunteer_one_field_success(self):
        # Pre Assert
        volunteer_before = townhall_services.VolunteerServices.get_volunteer(id=1)
        assert volunteer_before.first_name == "Zamorak"
        assert volunteer_before.last_name == "Red"
        assert volunteer_before.email == "zamorak.red@gmail.com"
        assert volunteer_before.gender == "M"
        split_string = (
            "pbkdf2_sha256$320000$eERGy7Egdf2$"
            "Rh6s7lqJXJH7dZJsZUZ7ix77E6EsHZaFL3Q8vPBvmfI="
        )
        assert volunteer_before.password == split_string
        assert volunteer_before.is_active is True

        # Arrange
        update_volunteer_data = UpdateVolunteerData(id=1, first_name="John")

        # Act
        townhall_services.VolunteerServices.update_volunteer(update_volunteer_data)

        # Assert
        volunteer_after = townhall_models.Volunteer.objects.get(id=1)
        assert volunteer_after.first_name == "John"
        assert volunteer_after.last_name == "Red"
        assert volunteer_after.email == "zamorak.red@gmail.com"
        assert volunteer_after.gender == "M"
        split_string = (
            "pbkdf2_sha256$320000$eERGy7Egdf2$"
            "Rh6s7lqJXJH7dZJsZUZ7ix77E6EsHZaFL3Q8vPBvmfI="
        )
        assert volunteer_before.password == split_string
        assert volunteer_after.is_active is True

    def test_update_volunteer_all_fields_success(self):
        # Pre Assert
        volunteer_before = townhall_services.VolunteerServices.get_volunteer(id=1)
        assert volunteer_before.first_name == "Zamorak"
        assert volunteer_before.last_name == "Red"
        assert volunteer_before.email == "zamorak.red@gmail.com"
        assert volunteer_before.gender == "M"
        split_string = (
            "pbkdf2_sha256$320000$eERGy7Egdf2$"
            "Rh6s7lqJXJH7dZJsZUZ7ix77E6EsHZaFL3Q8vPBvmfI="
        )
        assert volunteer_before.password == split_string
        assert volunteer_before.is_active is True

        # Arrange
        update_volunteer_data = UpdateVolunteerData(
            id=1,
            first_name="John",
            last_name="Doe",
            gender="F",
            email="john.doe@example.com",
            is_active=False,
        )

        # Act
        townhall_services.VolunteerServices.update_volunteer(update_volunteer_data)

        # Assert
        volunteer_after = townhall_models.Volunteer.objects.get(id=1)
        assert volunteer_after.first_name == "John"
        assert volunteer_after.last_name == "Doe"
        assert volunteer_after.email == "john.doe@example.com"
        assert volunteer_after.gender == "F"
        split_string = (
            "pbkdf2_sha256$320000$eERGy7Egdf2$"
            "Rh6s7lqJXJH7dZJsZUZ7ix77E6EsHZaFL3Q8vPBvmfI="
        )
        assert volunteer_before.password == split_string
        assert volunteer_after.is_active is False

    @patch("myapi.dao.VolunteerDao.update_volunteer")
    def test_update_volunteer_failed_not_found(self, mock_update_volunteer):
        # Arrange
        mock_update_volunteer.side_effect = townhall_models.Volunteer.DoesNotExist
        update_volunteer_data = UpdateVolunteerData(
            id=999, first_name="John"  # Assuming this ID does not exist
        )

        # Act & Assert
        with self.assertRaises(ValidationError) as context:
            townhall_services.VolunteerServices.update_volunteer(update_volunteer_data)

        # Assert
        id = update_volunteer_data.id
        assert (
            str(context.exception)
            == f"['Volunteer with the given id: {id}, does not exist.']"
        )

    def test_delete_volunteer_success(self):
        # Pre Assert
        volunteer_before = townhall_services.VolunteerServices.get_volunteer(id=1)
        assert volunteer_before.first_name == "Zamorak"
        assert volunteer_before.last_name == "Red"
        assert volunteer_before.email == "zamorak.red@gmail.com"
        assert volunteer_before.gender == "M"
        split_string = (
            "pbkdf2_sha256$320000$eERGy7Egdf2$"
            "Rh6s7lqJXJH7dZJsZUZ7ix77E6EsHZaFL3Q8vPBvmfI="
        )
        assert volunteer_before.password == split_string
        assert volunteer_before.is_active is True

        # Arrange
        volunteer_id = 1

        # Act
        townhall_services.VolunteerServices.delete_volunteer(volunteer_id)

        # Assert
        with self.assertRaises(townhall_models.Volunteer.DoesNotExist):
            townhall_models.Volunteer.objects.get(id=1)

    @patch("myapi.dao.VolunteerDao.delete_volunteer")
    def test_delete_volunteer_failed_not_found(self, mock_delete_volunteer):
        # Arrange
        mock_delete_volunteer.side_effect = townhall_models.Volunteer.DoesNotExist
        volunteer_id = 999  # Assuming this ID does not exist

        # Act & Assert
        with self.assertRaises(ValidationError) as context:
            townhall_services.VolunteerServices.delete_volunteer(volunteer_id)

        # Assert
        assert (
            str(context.exception)
            == f"['Volunteer with the given id: {volunteer_id}, does not exist.']"
        )

    @patch("myapi.services.VolunteerServices.authenticate_volunteer")
    @patch("myapi.services.VolunteerServices.validate_volunteer")
    def test_change_volunteers_password_success(
        self, mock_validate_volunteer, mock_authenticate_volunteer
    ):
        # Pre Arrange
        # Creating a Volunteer without a fixture to know the password pre hash
        townhall_models.Volunteer.objects.create(
            id=3,
            first_name="Bruce",
            last_name="Wayne",
            gender="M",
            email="batman@gmail.com",
            password=make_password("ImBatman99"),
        )

        # Pre Assert
        volunteer_before = townhall_services.VolunteerServices.get_volunteer(id=3)
        assert volunteer_before.first_name == "Bruce"
        assert volunteer_before.last_name == "Wayne"
        assert volunteer_before.email == "batman@gmail.com"
        assert volunteer_before.gender == "M"
        assert check_password("ImBatman99", volunteer_before.password)

        # Arrange
        changePasswordData = ChangeVolunteerPasswordData(
            id=3,
            email="batman@gmail.com",
            curr_password="ImBatman99",
            new_password="BruceWayne00",
        )
        # Ensure that these two methods always succeed and don't cause an error
        mock_authenticate_volunteer.return_value = (
            townhall_services.VolunteerServices.get_volunteer(id=3)
        )
        mock_validate_volunteer.return_value = None

        # Act
        townhall_services.VolunteerServices.change_volunteers_password(
            changePasswordData
        )

        # Assert
        volunteer_after = townhall_services.VolunteerServices.get_volunteer(id=3)
        assert volunteer_after.first_name == "Bruce"
        assert volunteer_after.last_name == "Wayne"
        assert volunteer_after.email == "batman@gmail.com"
        assert volunteer_after.gender == "M"
        assert check_password("BruceWayne00", volunteer_after.password)

    @patch("myapi.services.VolunteerServices.authenticate_volunteer")
    @patch("myapi.services.VolunteerServices.validate_volunteer")
    def test_change_volunteers_password_failed_authentication(
        self, mock_validate_volunteer, mock_authenticate_volunteer
    ):
        # Arrange
        mock_authenticate_volunteer.return_value = None  # Fail
        mock_validate_volunteer.return_value = None

        changePasswordData = (
            ChangeVolunteerPasswordData(  # Irrelevant, does not get checked
                id=3,
                email="batman@gmail.com",
                curr_password="ImBatman99",
                new_password="BruceWayne00",
            )
        )

        # Act & Assert
        with self.assertRaises(ValidationError) as context:
            townhall_services.VolunteerServices.change_volunteers_password(
                changePasswordData
            )

        # Assert
        assert (
            str(context.exception)
            == "['Volunteer could not be authenticated, try again later']"
        )

    @patch("myapi.services.VolunteerServices.authenticate_volunteer")
    @patch("myapi.services.VolunteerServices.validate_volunteer")
    def test_change_volunteers_password_failed_validation(
        self, mock_validate_volunteer, mock_authenticate_volunteer
    ):
        # Arrange
        mock_authenticate_volunteer.return_value = (
            townhall_services.VolunteerServices.get_volunteer(id=2)
        )
        mock_validate_volunteer.side_effect = ValidationError("Random Error Message")

        changePasswordData = (
            ChangeVolunteerPasswordData(  # Irrelevant, does not get checked
                id=3,
                email="batman@gmail.com",
                curr_password="ImBatman99",
                new_password="BruceWayne00",
            )
        )

        # Act & Assert
        with self.assertRaises(ValidationError) as context:
            townhall_services.VolunteerServices.change_volunteers_password(
                changePasswordData
            )

        # Assert
        assert str(context.exception) == "['Random Error Message']"

    def test_authenticate_volunteer_success(self):
        # Pre Arrange
        # Creating a Volunteer without a fixture to know the password pre hash
        townhall_models.Volunteer.objects.create(
            id=3,
            first_name="Bruce",
            last_name="Wayne",
            gender="M",
            email="batman@gmail.com",
            password=make_password("ImBatman99"),
        )

        # Pre Assert
        volunteer_before = townhall_services.VolunteerServices.get_volunteer(id=3)
        assert volunteer_before.first_name == "Bruce"
        assert volunteer_before.last_name == "Wayne"
        assert volunteer_before.email == "batman@gmail.com"
        assert volunteer_before.gender == "M"
        assert check_password("ImBatman99", volunteer_before.password)

        # Arrange
        email = "batman@gmail.com"
        password = "ImBatman99"

        # Act
        returned_volunteer = townhall_services.VolunteerServices.authenticate_volunteer(
            email, password
        )

        # Assert
        assert returned_volunteer.first_name == "Bruce"
        assert returned_volunteer.last_name == "Wayne"
        assert returned_volunteer.email == "batman@gmail.com"
        assert returned_volunteer.gender == "M"
        assert check_password("ImBatman99", returned_volunteer.password)

    def test_authenticate_volunteer_failed_wrong_password(self):
        # Arrange
        email = "zamorak.red@gmail.com"
        password = "something_wrong1234"

        # Act & Assert
        volunteer = townhall_services.VolunteerServices.authenticate_volunteer(
            email, password
        )

        # Assert
        assert volunteer is None

    def test_authenticate_volunteer_failed_inactive(self):
        # Pre Arrange
        # Creating a Volunteer without a fixture to know the password pre hash
        townhall_models.Volunteer.objects.create(
            id=3,
            first_name="Bruce",
            last_name="Wayne",
            gender="M",
            email="batman@gmail.com",
            password=make_password("ImBatman99"),
            is_active=False,
        )

        # Pre Assert
        volunteer_before = townhall_services.VolunteerServices.get_volunteer(id=3)
        assert volunteer_before.first_name == "Bruce"
        assert volunteer_before.last_name == "Wayne"
        assert volunteer_before.email == "batman@gmail.com"
        assert volunteer_before.gender == "M"
        assert volunteer_before.is_active is False
        assert check_password("ImBatman99", volunteer_before.password)

        # Arrange
        email = "batman@gmail.com"
        password = "ImBatman99"

        # Act & Assert
        with self.assertRaises(ValidationError) as context:
            townhall_services.VolunteerServices.authenticate_volunteer(email, password)

        # Assert
        assert str(context.exception) == "['Account is inactive.']"

    def test_validate_volunteer_success(self):
        # Arrange
        valid_email = "interstellar@gmail.com"
        valid_password = "Qwertyuiop1."

        # Act & Assert
        try:
            townhall_services.VolunteerServices.validate_volunteer(
                valid_email, valid_password
            )
        except ValidationError:
            self.fail("ValidationError raised incorrectly")

    def test_validate_volunteer_failed_invalid_email(self):
        # Arrange
        invalid_email = "interstellar"
        valid_password = "Qwertyuiop1."

        # Act & Assert
        with self.assertRaises(ValidationError) as context:
            townhall_services.VolunteerServices.validate_volunteer(
                invalid_email, valid_password
            )

        # Assert
        assert str(context.exception) == "['Invalid email format.']"

    def test_validate_volunteer_failed_invalid_password(self):
        # Arrange
        valid_email = "interstellar@gmail.com"
        invalid_password = "qwer"

        # Act & Assert
        with self.assertRaises(ValidationError) as context:
            townhall_services.VolunteerServices.validate_volunteer(
                valid_email, invalid_password
            )

        # Assert
        assert str(context.exception) == "['Invalid password.']"

    def test_validate_volunteer_failed_similar_password_and_email(self):
        # Arrange
        invalid_email = "interstellar5@gmail.com"
        invalid_password = "Interstellar5"

        # Act & Assert
        with self.assertRaises(ValidationError) as context:
            townhall_services.VolunteerServices.validate_volunteer(
                invalid_email, invalid_password
            )

        # Assert
        assert str(context.exception) == "['Password is too similar to the email.']"


# ***!!! KEYNOTE:
#        The testing done is NOT full coverage for methods involving the cache
#        This will need to be done in the future.
