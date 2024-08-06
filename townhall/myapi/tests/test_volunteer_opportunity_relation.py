from django.test import TestCase
from myapi import models as townhall_models
from myapi import services as townhall_services
from datetime import datetime
from django.utils import timezone

# Volunteer Opportunity Relationship

# Testing ALL tests "python manage.py test myapi.tests"
# Testing ONLY Volunteer Opportunity Relationship "python manage.py test myapi.tests.test_volunteer_opportunity_relation"

class TestVolunteerOpportunityModel(TestCase):
    def setUp(self):
        townhall_models.Volunteer.objects.create(id=1, first_name="Zamorak", last_name="Red", gender="M", email="zamorak.red@gmail.com")
        townhall_models.Volunteer.objects.create(id=2, first_name="Guthix", last_name="Green", gender="F", email="guthix_green@hotmail.ca")
        townhall_models.Volunteer.objects.create(id=3, first_name="Harvey", last_name="Spector", gender="M", email="harveyspector@outlook.com")

        townhall_models.Opportunity.objects.create(id=1, name="Food bank", time=timezone.make_aware(datetime(2024, 7, 20, 10, 0)), description="Deliver food", location="Vancouver")
        townhall_models.Opportunity.objects.create(id=2, name="Hygiene", time=timezone.make_aware(datetime(2024, 7, 20, 10, 0)), description="Deliver clothes", location="East Vancouver")
        townhall_models.Opportunity.objects.create(id=3, name="Community Clean Up", time=timezone.make_aware(datetime(2024, 7, 20, 10, 0)), description="Clean up the neighborhood", location="West Vancouver")

    def test_add_volunteer_to_one_opportunity(self):
        opportunity = townhall_services.OpportunityServices.get_opportunity(id=1)
        volunteer = townhall_services.VolunteerServices.get_volunteer(id=1)

        volunteers_before = opportunity.volunteers.all()
        assert len(volunteers_before) == 0

        opportunities_before = volunteer.volunteers.all()
        assert len(opportunities_before) == 0

        townhall_services.OpportunityServices.add_volunteer_to_opportunity(1, 1)

        volunteers = opportunity.volunteers.all()
        assert len(volunteers) == 1

        opportunities = volunteer.volunteers.all()
        assert len(opportunities) == 1

    def test_add_volunteer_to_many_opportunities(self):
        opportunity1 = townhall_services.OpportunityServices.get_opportunity(id=1)
        opportunity2 = townhall_services.OpportunityServices.get_opportunity(id=2)
        opportunity3 = townhall_services.OpportunityServices.get_opportunity(id=3)
        volunteer = townhall_services.VolunteerServices.get_volunteer(id=1)

        volunteers1_before = opportunity1.volunteers.all()
        assert len(volunteers1_before) == 0
        volunteers2_before = opportunity2.volunteers.all()
        assert len(volunteers2_before) == 0
        volunteers3_before = opportunity3.volunteers.all()
        assert len(volunteers3_before) == 0

        opportunities_before = volunteer.volunteers.all()
        assert len(opportunities_before) == 0

        townhall_services.OpportunityServices.add_volunteer_to_opportunity(1, 1)
        townhall_services.OpportunityServices.add_volunteer_to_opportunity(2, 1)
        townhall_services.OpportunityServices.add_volunteer_to_opportunity(3, 1)

        volunteers1 = opportunity1.volunteers.all()
        assert len(volunteers1) == 1
        volunteers2 = opportunity2.volunteers.all()
        assert len(volunteers2) == 1
        volunteers3 = opportunity3.volunteers.all()
        assert len(volunteers3) == 1

        opportunities = volunteer.volunteers.all()
        assert len(opportunities) == 3


    def test_add_many_volunteers_to_one_opportunity(self):
        opportunity = townhall_services.OpportunityServices.get_opportunity(id=1)
        volunteer1 = townhall_services.VolunteerServices.get_volunteer(id=1)
        volunteer2 = townhall_services.VolunteerServices.get_volunteer(id=2)
        volunteer3 = townhall_services.VolunteerServices.get_volunteer(id=3)

        volunteers_before = opportunity.volunteers.all()
        assert len(volunteers_before) == 0

        opportunties1_before = volunteer1.volunteers.all()
        assert len(opportunties1_before) == 0
        opportunties2_before = volunteer2.volunteers.all()
        assert len(opportunties2_before) == 0
        opportunties3_before = volunteer3.volunteers.all()
        assert len(opportunties3_before) == 0

        townhall_services.OpportunityServices.add_volunteer_to_opportunity(1, 1)
        townhall_services.OpportunityServices.add_volunteer_to_opportunity(1, 2)
        townhall_services.OpportunityServices.add_volunteer_to_opportunity(1, 3)

        volunteers = opportunity.volunteers.all()
        assert len(volunteers) == 3

        opportunties1 = volunteer1.volunteers.all()
        assert len(opportunties1) == 1
        opportunties2 = volunteer2.volunteers.all()
        assert len(opportunties2) == 1
        opportunties3 = volunteer3.volunteers.all()
        assert len(opportunties3) == 1


    def test_remove_one_volunteer(self):
        opportunity = townhall_services.OpportunityServices.get_opportunity(id=1)
        volunteer1 = townhall_services.VolunteerServices.get_volunteer(id=1)
        volunteer2 = townhall_services.VolunteerServices.get_volunteer(id=2)

        volunteers_before = opportunity.volunteers.all()
        assert len(volunteers_before) == 0

        opportunties1_before = volunteer1.volunteers.all()
        assert len(opportunties1_before) == 0
        opportunties2_before = volunteer2.volunteers.all()
        assert len(opportunties2_before) == 0

        townhall_services.OpportunityServices.add_volunteer_to_opportunity(1, 1)
        townhall_services.OpportunityServices.add_volunteer_to_opportunity(1, 2)

        volunteers = opportunity.volunteers.all()
        assert len(volunteers) == 2

        opportunties1 = volunteer1.volunteers.all()
        assert len(opportunties1) == 1
        opportunties2 = volunteer2.volunteers.all()
        assert len(opportunties2) == 1

        townhall_services.OpportunityServices.remove_volunteer_from_opportunity(1, 1)

        volunteers_after = opportunity.volunteers.all()
        assert len(volunteers_after) == 1

        opportunties1_after = volunteer1.volunteers.all()
        assert len(opportunties1_after) == 0
        opportunties2_after = volunteer2.volunteers.all()
        assert len(opportunties2_after) == 1


    def test_remove_all_volunteers(self):
        opportunity = townhall_services.OpportunityServices.get_opportunity(id=1)
        volunteer1 = townhall_services.VolunteerServices.get_volunteer(id=1)
        volunteer2 = townhall_services.VolunteerServices.get_volunteer(id=2)

        volunteers_before = opportunity.volunteers.all()
        assert len(volunteers_before) == 0

        opportuntities1_before = volunteer1.volunteers.all()
        assert len(opportuntities1_before) == 0
        opportuntities2_before = volunteer2.volunteers.all()
        assert len(opportuntities2_before) == 0

        townhall_services.OpportunityServices.add_volunteer_to_opportunity(1, 1)
        townhall_services.OpportunityServices.add_volunteer_to_opportunity(1, 2)

        volunteers = opportunity.volunteers.all()
        assert len(volunteers) == 2

        opportuntities1 = volunteer1.volunteers.all()
        assert len(opportuntities1) == 1
        opportuntities2 = volunteer2.volunteers.all()
        assert len(opportuntities2) == 1

        townhall_services.OpportunityServices.remove_all_volunteers_from_opportunity(1)

        volunteer_after = opportunity.volunteers.all()
        assert len(volunteer_after) == 0

        opportuntities1_after = volunteer1.volunteers.all()
        assert len(opportuntities1_after) == 0
        opportuntities2_after = volunteer2.volunteers.all()
        assert len(opportuntities2_after) == 0
