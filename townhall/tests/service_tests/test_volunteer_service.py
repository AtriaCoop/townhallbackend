from django.test import TestCase
from django.core.management import call_command

from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password, make_password

from myapi.models import Volunteer as vol_mod
from myapi.models import Opportunity as opp_mod
from myapi.services import VolunteerServices as vol_serv

from myapi.types import CreateVolunteerData
from myapi.types import UpdateVolunteerData
from myapi.types import FilterVolunteerData
from myapi.types import ChangeVolunteerPasswordData

from myapi.types import FilteredOpportunityData


# VOLUNTEER

# Testing ALL tests "python manage.py test myapi.tests"
# Testing ONLY volunteer "python manage.py test myapi.tests.test_volunteer"


class TestVolunteerModel(TestCase):
    def setUp(self):
        # Arrange (For all non-mock tests)
        call_command("loaddata", "volunteer_fixture.json")
        call_command("loaddata", "opportunity_fixture.json")

    def test_get_volunteer_found(self):
        # Act
        volunteer = vol_serv.get_volunteer(id=1)

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
        mock_get_volunteer.side_effect = vol_mod.DoesNotExist
        volunteer_id = 999  # Assuming this ID does not exist

        # Act & Assert
        with self.assertRaises(ValidationError) as context:
            vol_serv.get_volunteer(volunteer_id)

        # Assert
        assert (
            str(context.exception)
            == f"['Volunteer with the given id: {volunteer_id}, does not exist.']"
        )

    def test_get_all_opportunities_of_volunteer_found_no_filters(self):
        # Arrange
        opportunity1 = opp_mod.objects.get(id=1)
        opportunity2 = opp_mod.objects.get(id=2)
        volunteer = vol_serv.get_volunteer(id=1)
        opportunity1.volunteers.add(volunteer)
        opportunity2.volunteers.add(volunteer)
        filtered_opportunity_data = FilteredOpportunityData(volunteer_id=1)

        # Act
        opportunities = vol_serv.get_all_filtered_opportunities_of_a_volunteer(
            filtered_opportunity_data
        )

        # Assert
        assert len(opportunities) == 2
        ids = [opportunity.id for opportunity in opportunities]
        assert set(ids) == {1, 2}

    def test_get_all_opportunities_of_volunteer_found_one_filter(self):
        # Arrange
        opportunity1 = opp_mod.objects.get(id=1)
        opportunity2 = opp_mod.objects.get(id=2)
        volunteer = vol_serv.get_volunteer(id=1)
        opportunity1.volunteers.add(volunteer)
        opportunity2.volunteers.add(volunteer)
        filtered_opportunity_data = FilteredOpportunityData(
            location="Van", volunteer_id=1
        )

        # Act
        opportunities = vol_serv.get_all_filtered_opportunities_of_a_volunteer(
            filtered_opportunity_data
        )

        # Assert
        assert len(opportunities) == 2
        ids = [opportunity.id for opportunity in opportunities]
        assert set(ids) == {1, 2}

    def test_get_all_opportunities_of_volunteer_found_all_filters(self):
        # Arrange
        opportunity1 = opp_mod.objects.get(id=1)
        opportunity2 = opp_mod.objects.get(id=2)
        volunteer = vol_serv.get_volunteer(id=1)
        opportunity1.volunteers.add(volunteer)
        opportunity2.volunteers.add(volunteer)
        filtered_opportunity_data = FilteredOpportunityData(
            title="ygien",
            starting_start_time="2024-07-19T10:00:00Z",
            starting_end_time="2024-07-21T10:00:00Z",
            ending_start_time="2024-07-19T21:45:00Z",
            ending_end_time="2024-07-21T21:45:00Z",
            location="Vancouver",
            organization_id=1,
            volunteer_id=1,
        )

        # Act
        opportunities = vol_serv.get_all_filtered_opportunities_of_a_volunteer(
            filtered_opportunity_data
        )

        # Assert
        assert len(opportunities) == 1
        ids = [opportunity.id for opportunity in opportunities]
        assert set(ids) == {2}

    @patch("myapi.dao.VolunteerDao.get_all_filtered_opportunities_of_a_volunteer")
    def test_get_all_opportunities_of_volunteer_not_found(
        self, mock_get_all_filtered_opportunities_of_a_volunteer
    ):
        # Arrange
        mock_get_all_filtered_opportunities_of_a_volunteer.return_value = (
            opp_mod.objects.none()
        )
        filtered_opportunity_data = FilteredOpportunityData(volunteer_id=1)

        # Act
        opportunities = vol_serv.get_all_filtered_opportunities_of_a_volunteer(
            filtered_opportunity_data
        )

        # Assert
        assert len(opportunities) == 0

    @patch("myapi.services.VolunteerServices.validate_volunteer")
    def test_create_volunteer_validation_error(self, mock_validate_volunteer):
        # Arrange
        mock_validate_volunteer.side_effect = ValidationError("Random Error Message")
        create_volunteer_data = CreateVolunteerData(
            first_name="John",
            last_name="Doe",
            gender="F",
            email="john.doe@example.com",
            password="JohnDoe987",
        )

        # Act & Assert
        with self.assertRaises(ValidationError) as context:
            vol_serv.create_volunteer(create_volunteer_data)

        # Assert
        assert str(context.exception) == "['Random Error Message']"

    def test_add_volunteer_to_opportunity_success(self):
        # Act
        vol_serv.add_volunteer_to_opportunity(1, 1)

        # Assert
        volunteer = vol_serv.get_volunteer(id=1)
        assert len(volunteer.opportunities.all()) == 1
        ids = [opportunity.id for opportunity in volunteer.opportunities.all()]
        assert set(ids) == {1}

    @patch("myapi.dao.VolunteerDao.add_volunteer_to_opportunity")
    def test_add_volunteer_to_opportunity_volunteer_not_found(
        self, mock_add_volunteer_to_opportunity
    ):
        # Arrange
        mock_add_volunteer_to_opportunity.side_effect = vol_mod.DoesNotExist
        volunteer_id = 999  # Assuming this ID does not exist

        # Act & Assert
        with self.assertRaises(ValidationError) as context:
            vol_serv.add_volunteer_to_opportunity(volunteer_id, 1)

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
        mock_add_volunteer_to_opportunity.side_effect = opp_mod.DoesNotExist
        opportunity_id = 999  # Assuming this ID does not exist

        # Act & Assert
        with self.assertRaises(ValidationError) as context:
            vol_serv.add_volunteer_to_opportunity(1, opportunity_id)

        # Assert
        assert (
            str(context.exception)
            == f"['Opportunity with the given id: {opportunity_id}, does not exist.']"
        )

    def test_remove_volunteer_from_opportunity_success(self):
        # Arrange
        opportunity1 = opp_mod.objects.get(id=1)
        opportunity2 = opp_mod.objects.get(id=2)
        volunteer = vol_serv.get_volunteer(id=1)
        opportunity1.volunteers.add(volunteer)
        opportunity2.volunteers.add(volunteer)

        # Act
        vol_serv.remove_volunteer_from_opportunity(1, 1)

        # Assert
        volunteer = vol_serv.get_volunteer(id=1)
        assert len(volunteer.opportunities.all()) == 1
        ids = [opportunity.id for opportunity in volunteer.opportunities.all()]
        assert set(ids) == {2}

    @patch("myapi.dao.VolunteerDao.remove_volunteer_from_opportunity")
    def test_remove_volunteer_from_opportunity_volunteer_not_found(
        self, mock_remove_volunteer_from_opportunity
    ):
        # Arrange
        mock_remove_volunteer_from_opportunity.side_effect = vol_mod.DoesNotExist
        volunteer_id = 999  # Assuming this ID does not exist

        # Act & Assert
        with self.assertRaises(ValidationError) as context:
            vol_serv.remove_volunteer_from_opportunity(volunteer_id, 1)

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
        mock_remove_volunteer_from_opportunity.side_effect = opp_mod.DoesNotExist
        opportunity_id = 999  # Assuming this ID does not exist

        # Act & Assert
        with self.assertRaises(ValidationError) as context:
            vol_serv.add_volunteer_to_opportunity(1, opportunity_id)

        # Assert
        assert (
            str(context.exception)
            == f"['Opportunity with the given id: {opportunity_id}, does not exist.']"
        )

    def test_update_volunteer_one_field_success(self):
        # Pre Assert
        volunteer_before = vol_serv.get_volunteer(id=1)
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
        vol_serv.update_volunteer(update_volunteer_data)

        # Assert
        volunteer_after = vol_mod.objects.get(id=1)
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
        volunteer_before = vol_serv.get_volunteer(id=1)
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
        vol_serv.update_volunteer(update_volunteer_data)

        # Assert
        volunteer_after = vol_mod.objects.get(id=1)
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
        mock_update_volunteer.side_effect = vol_mod.DoesNotExist
        update_volunteer_data = UpdateVolunteerData(
            id=999, first_name="John"  # Assuming this ID does not exist
        )

        # Act & Assert
        with self.assertRaises(ValidationError) as context:
            vol_serv.update_volunteer(update_volunteer_data)

        # Assert
        id = update_volunteer_data.id
        assert (
            str(context.exception)
            == f"['Volunteer with the given id: {id}, does not exist.']"
        )

    def test_delete_volunteer_success(self):
        # Pre Assert
        volunteer_before = vol_serv.get_volunteer(id=1)
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
        vol_serv.delete_volunteer(volunteer_id)

        # Assert
        with self.assertRaises(vol_mod.DoesNotExist):
            vol_mod.objects.get(id=1)

    @patch("myapi.dao.VolunteerDao.delete_volunteer")
    def test_delete_volunteer_failed_not_found(self, mock_delete_volunteer):
        # Arrange
        mock_delete_volunteer.side_effect = vol_mod.DoesNotExist
        volunteer_id = 999  # Assuming this ID does not exist

        # Act & Assert
        with self.assertRaises(ValidationError) as context:
            vol_serv.delete_volunteer(volunteer_id)

        # Assert
        assert (
            str(context.exception)
            == f"['Volunteer with the given id: {volunteer_id}, does not exist.']"
        )

    def test_get_all_volunteers_all_filters_success_found(self):
        # Arrange
        filter_volunteer_data = FilterVolunteerData(
            first_name="amor",
            last_name="Re",
            email="zamorak.red@gmail.com",
            gender="M",
            is_active=True,
        )

        # Act
        volunteers = vol_serv.get_all_volunteers_optional_filter(filter_volunteer_data)

        # Assert
        assert len(volunteers) == 1
        ids = [volunteer.id for volunteer in volunteers]
        assert set(ids) == {1}

    def test_get_all_volunteers_one_filter_success_found(self):
        # Arrange
        filter_volunteer_data = FilterVolunteerData(is_active=True)

        # Act
        volunteers = vol_serv.get_all_volunteers_optional_filter(filter_volunteer_data)

        # Assert
        assert len(volunteers) == 2
        ids = [volunteer.id for volunteer in volunteers]
        assert set(ids) == {1, 2}

    def test_get_all_volunteers_all_filters_success_not_found(self):
        # Arrange
        filter_volunteer_data = FilterVolunteerData(
            first_name="amor",
            last_name="Re",
            email="zamorak.red@gmail.co",
            gender="M",
            is_active=True,
        )

        # Act
        volunteers = vol_serv.get_all_volunteers_optional_filter(filter_volunteer_data)

        # Assert
        assert len(volunteers) == 0

    def test_get_all_volunteers_one_filter_success_not_found(self):
        # Arrange
        filter_volunteer_data = FilterVolunteerData(is_active=False)

        # Act
        volunteers = vol_serv.get_all_volunteers_optional_filter(filter_volunteer_data)

        # Assert
        assert len(volunteers) == 0

    def test_get_all_volunteers_no_filters_success(self):
        # Act
        volunteers = vol_serv.get_all_volunteers_optional_filter(None)

        # Assert
        assert len(volunteers) == 2
        ids = [volunteer.id for volunteer in volunteers]
        assert set(ids) == {1, 2}

    @patch("myapi.services.VolunteerServices.authenticate_volunteer")
    @patch("myapi.services.VolunteerServices.validate_volunteer")
    def test_change_volunteers_password_success(
        self, mock_validate_volunteer, mock_authenticate_volunteer
    ):
        # Pre Arrange
        # Creating a Volunteer without a fixture to know the password pre hash
        vol_mod.objects.create(
            id=3,
            first_name="Bruce",
            last_name="Wayne",
            gender="M",
            email="batman@gmail.com",
            password=make_password("ImBatman99"),
        )

        # Pre Assert
        volunteer_before = vol_serv.get_volunteer(id=3)
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
        mock_authenticate_volunteer.return_value = vol_serv.get_volunteer(id=3)
        mock_validate_volunteer.return_value = None

        # Act
        vol_serv.change_volunteers_password(changePasswordData)

        # Assert
        volunteer_after = vol_serv.get_volunteer(id=3)
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
            vol_serv.change_volunteers_password(changePasswordData)

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
        mock_authenticate_volunteer.return_value = vol_serv.get_volunteer(id=2)
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
            vol_serv.change_volunteers_password(changePasswordData)

        # Assert
        assert str(context.exception) == "['Random Error Message']"

    def test_authenticate_volunteer_success(self):
        # Pre Arrange
        # Creating a Volunteer without a fixture to know the password pre hash
        vol_mod.objects.create(
            id=3,
            first_name="Bruce",
            last_name="Wayne",
            gender="M",
            email="batman@gmail.com",
            password=make_password("ImBatman99"),
        )

        # Pre Assert
        volunteer_before = vol_serv.get_volunteer(id=3)
        assert volunteer_before.first_name == "Bruce"
        assert volunteer_before.last_name == "Wayne"
        assert volunteer_before.email == "batman@gmail.com"
        assert volunteer_before.gender == "M"
        assert check_password("ImBatman99", volunteer_before.password)

        # Arrange
        email = "batman@gmail.com"
        password = "ImBatman99"

        # Act
        returned_volunteer = vol_serv.authenticate_volunteer(email, password)

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
        volunteer = vol_serv.authenticate_volunteer(email, password)

        # Assert
        assert volunteer is None

    def test_authenticate_volunteer_failed_inactive(self):
        # Pre Arrange
        # Creating a Volunteer without a fixture to know the password pre hash
        vol_mod.objects.create(
            id=3,
            first_name="Bruce",
            last_name="Wayne",
            gender="M",
            email="batman@gmail.com",
            password=make_password("ImBatman99"),
            is_active=False,
        )

        # Pre Assert
        volunteer_before = vol_serv.get_volunteer(id=3)
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
            vol_serv.authenticate_volunteer(email, password)

        # Assert
        assert str(context.exception) == "['Account is inactive.']"

    def test_validate_volunteer_success(self):
        # Arrange
        valid_email = "interstellar@gmail.com"
        valid_password = "Qwertyuiop1."

        # Act & Assert
        try:
            vol_serv.validate_volunteer(valid_email, valid_password)
        except ValidationError:
            self.fail("ValidationError raised incorrectly")

    def test_validate_volunteer_failed_invalid_email(self):
        # Arrange
        invalid_email = "interstellar"
        valid_password = "Qwertyuiop1."

        # Act & Assert
        with self.assertRaises(ValidationError) as context:
            vol_serv.validate_volunteer(invalid_email, valid_password)

        # Assert
        assert str(context.exception) == "['Invalid email format.']"

    def test_validate_volunteer_failed_invalid_password(self):
        # Arrange
        valid_email = "interstellar@gmail.com"
        invalid_password = "qwer"

        # Act & Assert
        with self.assertRaises(ValidationError) as context:
            vol_serv.validate_volunteer(valid_email, invalid_password)

        # Assert
        assert str(context.exception) == "['Invalid password.']"

    def test_validate_volunteer_failed_similar_password_and_email(self):
        # Arrange
        invalid_email = "interstellar5@gmail.com"
        invalid_password = "Interstellar5"

        # Act & Assert
        with self.assertRaises(ValidationError) as context:
            vol_serv.validate_volunteer(invalid_email, invalid_password)

        # Assert
        assert str(context.exception) == "['Password is too similar to the email.']"


# ***!!! KEYNOTE:
#        The testing done is NOT full coverage for methods involving the cache
#        This will need to be done in the future.
