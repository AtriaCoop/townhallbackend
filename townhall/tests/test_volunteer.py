from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from myapi import models as townhall_models
from myapi import services as townhall_services

# VOLUNTEER

# Testing ALL tests "python manage.py test myapi.tests"
# Testing ONLY volunteer "python manage.py test myapi.tests.test_volunteer"

class TestVolunteerModel(TestCase):
    def setUp(self):
        townhall_models.Volunteer.objects.create(id=1, first_name="Zamorak", last_name="Red", email="zamorak.red@gmail.com", gender="M")
        townhall_models.Volunteer.objects.create(id=2, first_name="Guthix", last_name="Green", email="guthix_green@hotmail.ca", gender="F")

    def test_get_volunteer(self):
        volunteer_1 = townhall_services.VolunteerServices.get_volunteer(id=1)
        assert volunteer_1.first_name == "Zamorak"
        assert volunteer_1.last_name == "Red"
        assert volunteer_1.email == "zamorak.red@gmail.com"
        assert volunteer_1.gender == "M"

    def test_update_volunteer(self):
        # Step 1: Getting the volunteer and make sure it exists
        volunteer_before_update = townhall_services.VolunteerServices.get_volunteer(id=2)
        assert volunteer_before_update.first_name == "Guthix"
        assert volunteer_before_update.last_name == "Green"
        assert volunteer_before_update.email == "guthix_green@hotmail.ca"
        assert volunteer_before_update.gender == "F"
        
        # Step 2: Update
        update_volunteer_data = townhall_services.UpdateVolunteerData(
            id=2,
            first_name="Saradomin",
            last_name="Blue",
            email="saradomin.blue@gmail.com",
            gender="M"
        )
        townhall_services.VolunteerServices.update_volunteer(update_volunteer_data)

        # Step 3: Fetching volunteer and making sure the update was successful
        # Additional test : Delete step 2 and try to GET volunteer_before_update information and it should pass
        updated_volunteer = townhall_services.VolunteerServices.get_volunteer(id=2)
        assert updated_volunteer.first_name == "Saradomin"
        assert updated_volunteer.last_name == "Blue"
        assert updated_volunteer.email == "saradomin.blue@gmail.com"
        assert updated_volunteer.gender == "M"

    def test_delete_volunteer(self):
        # Step 1
        volunteer_1 = townhall_services.VolunteerServices.get_volunteer(id=1)
        assert volunteer_1.first_name == "Zamorak"
        assert volunteer_1.last_name == "Red"
        assert volunteer_1.email == "zamorak.red@gmail.com"
        assert volunteer_1.gender == "M"

        # Step 2
        townhall_services.VolunteerServices.delete_volunteer(id=1)
        assert townhall_services.VolunteerServices.get_volunteer(id=1) is None

    # Retrieving all volunteers
    def test_get_all_volunteers(self):
        volunteers = townhall_services.VolunteerServices.get_volunteers_all()
        assert len(volunteers) == 2, "There should be two volunteers"
        assert volunteers[0].first_name == "Zamorak"
        assert volunteers[1].first_name == "Guthix"

    # Retrieving all volunteers when there are none
    def test_get_all_volunteers_empty(self):
        # Clear all volunteers
        townhall_models.Volunteer.objects.all().delete()

        volunteers = townhall_services.VolunteerServices.get_volunteers_all()
        assert len(volunteers) == 0, "There should be no volunteers"

    # Tests for the PUT Endpoint

    # Test successfully updating a volunteer's information via PUT.
    def test_update_volunteer_success(self):
        
        updated_data = {
            "first_name": "Saradomin",
            "last_name": "Blue",
            "email": "saradomin.blue@gmail.com",
            "gender": "M"
        }
        response = self.client.put(
            reverse('update_volunteer', kwargs={'pk': 2}),
            updated_data,
            format='json',
            content_type='application/json'
        )

        # Print the response status code and data for debugging
        assert response.status_code == status.HTTP_200_OK
        assert response.data['first_name'] == "Saradomin"
        assert response.data['last_name'] == "Blue"
        assert response.data['email'] == "saradomin.blue@gmail.com"
        assert response.data['gender'] == "M"

    def test_update_volunteer_invalid_data(self):
        # Test updating a volunteer with invalid data via PUT.
        invalid_data = {
            "first_name": "",
            "last_name": "Blue",
            "email": "not-an-email",
            "gender": "X"
        }
        response = self.client.put(
            reverse('update_volunteer', kwargs={'pk': 2}),
            invalid_data,
            format='json',
            content_type='application/json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

