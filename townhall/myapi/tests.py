from django.test import TestCase
from myapi import models as townhall_models
from myapi import services as townhall_services
from datetime import datetime
from django.utils import timezone

# Run test class with "python manage.py test"

class TownhallTestCase(TestCase):
    def setUp(self):
        townhall_models.Volunteer.objects.create(id=1, first_name="Zamorak", last_name="Red", age=11, email="zamorak.red@gmail.com")
        townhall_models.Volunteer.objects.create(id=2, first_name="Guthix", last_name="Green", age=77, email="guthix_green@hotmail.ca")

        townhall_models.Opportunity.objects.create(id=1, name="Food bank", time=timezone.make_aware(datetime(2024, 7, 20, 10, 0)), description="Deliver food", location="Vancouver")
        townhall_models.Opportunity.objects.create(id=2, name="Hygiene", time=timezone.make_aware(datetime(2024, 7, 20, 10, 0)), description="Deliver clothes", location="East Vancouver")

# VOLUNTEER

    def test_get_volunteer(self):
        volunteer_1 = townhall_services.VolunteerServices.get_volunteer(id=1)
        assert volunteer_1.first_name == "Zamorak"
        assert volunteer_1.last_name == "Red"
        assert volunteer_1.age == 11
        assert volunteer_1.email == "zamorak.red@gmail.com"

    def test_update_volunteer(self):
        # Step 1: Getting the volunteer and make sure it exists
        volunteer_before_update = townhall_services.VolunteerServices.get_volunteer(id=2)
        assert volunteer_before_update.first_name == "Guthix"
        assert volunteer_before_update.last_name == "Green"
        assert volunteer_before_update.age == 77
        assert volunteer_before_update.email == "guthix_green@hotmail.ca"
        
        # Step 2: Update
        update_volunteer_data = townhall_services.UpdateVolunteerData(
            id=2,
            first_name="Saradomin",
            last_name="Blue",
            gender="Male",
            age=12,
            email="saradomin.blue@gmail.com"
        )
        townhall_services.VolunteerServices.update_volunteer(update_volunteer_data)

        # Step 3: Fetching volunteer and making sure the update was successful
        # Additional test : Delete step 2 and try to GET volunteer_before_update information and it should pass
        updated_volunteer = townhall_services.VolunteerServices.get_volunteer(id=2)
        assert updated_volunteer.first_name == "Saradomin"
        assert updated_volunteer.last_name == "Blue"
        assert updated_volunteer.age == 12
        assert updated_volunteer.email == "saradomin.blue@gmail.com"



# OPPORTUNITY

    def test_delete_volunteer(self):
        # Step 1
        volunteer_1 = townhall_services.VolunteerServices.get_volunteer(id=1)
        assert volunteer_1.first_name == "Zamorak"
        assert volunteer_1.last_name == "Red"
        assert volunteer_1.age == 11
        assert volunteer_1.email == "zamorak.red@gmail.com"

        # Step 2
        townhall_services.VolunteerServices.delete_volunteer(id=1)
        assert townhall_services.VolunteerServices.get_volunteer(id=1) is None




    def test_create_opportunity(self):
        townhall_models.Opportunity.objects.create(id=3, name="Community Clean Up", time=timezone.make_aware(datetime(2024, 7, 20, 10, 0)), description="Clean up the neighborhood", location="West Vancouver")

    def test_get_opportunity(self):
        opportunity = townhall_services.OpportunityServices.get_opportunity(id=1)
        assert opportunity.name == "Food bank"
        assert opportunity.time == timezone.make_aware(datetime(2024, 7, 20, 10, 0))
        assert opportunity.description == "Deliver food"
        assert opportunity.location == "Vancouver"
        

    def test_dummy_test(self):
        pass