from django.test import TestCase
from myapi import models as townhall_models
from myapi import services as townhall_services
from datetime import datetime
from django.utils import timezone

# OPPORTUNITY

# Testing ALL tests "python manage.py test tests"
# Testing ONLY opportunity "python manage.py test tests.test_opportunity"


class TestOpportunityModel(TestCase):
    def setUp(self):
        townhall_models.Opportunity.objects.create(
            id=1,
            title="Food bank",
            description="Deliver food",
            start_time=timezone.make_aware(datetime(2024, 7, 20, 10, 0)),
            end_time=timezone.make_aware(datetime(2024, 7, 20, 20, 30)),
            location="Vancouver",
        )
        townhall_models.Opportunity.objects.create(
            id=2,
            title="Hygiene",
            description="Deliver clothes",
            start_time=timezone.make_aware(datetime(2024, 7, 20, 10, 0)),
            end_time=timezone.make_aware(datetime(2024, 7, 20, 21, 45)),
            location="East Vancouver",
        )
        townhall_models.Opportunity.objects.create(
            id=3,
            title="Community Clean Up",
            description="Clean up the neighborhood",
            start_time=timezone.make_aware(datetime(2024, 7, 20, 10, 0)),
            end_time=timezone.make_aware(datetime(2024, 7, 20, 21, 15)),
            location="West Vancouver",
        )

        townhall_models.Volunteer.objects.create(
            id=1,
            first_name="Zamorak",
            last_name="Red",
            gender="M",
            email="zamorak.red@gmail.com",
        )
        townhall_models.Volunteer.objects.create(
            id=2,
            first_name="Guthix",
            last_name="Green",
            gender="F",
            email="guthix_green@hotmail.ca",
        )
        townhall_models.Volunteer.objects.create(
            id=3,
            first_name="Harvey",
            last_name="Spector",
            gender="M",
            email="harveyspector@outlook.com",
        )

    def test_get_opportunity(self):
        opportunity = townhall_services.OpportunityServices.get_opportunity(id=1)
        assert opportunity.title == "Food bank"
        assert opportunity.description == "Deliver food"
        assert opportunity.start_time == timezone.make_aware(
            datetime(2024, 7, 20, 10, 0)
        )
        assert opportunity.end_time == timezone.make_aware(
            datetime(2024, 7, 20, 20, 30)
        )
        assert opportunity.location == "Vancouver"

    def test_filtered_opportunity_name_and_time(self):
        starting_start_time = timezone.make_aware(datetime(2024, 7, 20, 0, 0))
        starting_end_time = timezone.make_aware(datetime(2024, 7, 20, 23, 59))
        filtered_opportunity_data = townhall_services.FilteredOpportunityData(
            title="Food",
            starting_start_time=starting_start_time,
            starting_end_time=starting_end_time,
        )
        opportunities = townhall_services.OpportunityServices.filtered_opportunity(
            filtered_opportunity_data
        )

        for o in opportunities:
            print(
                f"Opportunity: {o.title}, "
                f"Start Time: {o.start_time}, "
                f"Location: {o.location}"
            )

        # Assert that exactly only one opportunity is returned
        assert len(opportunities) == 1

        for opportunity in opportunities:
            assert "food" in opportunity.title.lower()  # Case insensitive check
            assert (
                starting_start_time <= opportunity.start_time <= starting_end_time
            )  # Time range check

    def test_delete_opportunity(self):
        # Step 1
        opportunity = townhall_services.OpportunityServices.get_opportunity(id=1)
        assert opportunity.title == "Food bank"
        assert opportunity.description == "Deliver food"
        assert opportunity.start_time == timezone.make_aware(
            datetime(2024, 7, 20, 10, 0)
        )
        assert opportunity.end_time == timezone.make_aware(
            datetime(2024, 7, 20, 20, 30)
        )
        assert opportunity.location == "Vancouver"

        # Step 2
        townhall_services.OpportunityServices.delete_opportunity(id=1)
        assert townhall_services.OpportunityServices.get_opportunity(id=1) is None

    def test_update_opportunity(self):
        # Step 1
        opportunity_before_update = (
            townhall_services.OpportunityServices.get_opportunity(id=3)
        )
        assert opportunity_before_update.title == "Community Clean Up"
        assert opportunity_before_update.description == "Clean up the neighborhood"
        assert opportunity_before_update.start_time == timezone.make_aware(
            datetime(2024, 7, 20, 10, 0)
        )
        assert opportunity_before_update.end_time == timezone.make_aware(
            datetime(2024, 7, 20, 21, 15)
        )
        assert opportunity_before_update.location == "West Vancouver"

        # Step 2
        update_opportunity_data = townhall_services.UpdateOpportunityData(
            id=3,
            title="Community Gardening",
            description="Planting some flowers in the community center",
            start_time=timezone.make_aware(datetime(2024, 8, 15, 2, 0)),
            end_time=timezone.make_aware(datetime(2024, 8, 15, 10, 30)),
            location="Richmond",
        )
        townhall_services.OpportunityServices.update_opportunity(
            id=3, update_opportunity_data=update_opportunity_data
        )

        # Step 3
        updated_opportunity = townhall_services.OpportunityServices.get_opportunity(
            id=3
        )
        assert updated_opportunity.title == "Community Gardening"
        assert (
            updated_opportunity.description
            == "Planting some flowers in the community center"
        )
        assert updated_opportunity.start_time == timezone.make_aware(
            datetime(2024, 8, 15, 2, 0)
        )
        assert updated_opportunity.end_time == timezone.make_aware(
            datetime(2024, 8, 15, 10, 30)
        )
        assert updated_opportunity.location == "Richmond"

    def test_add_volunteer_to_one_opportunity(self):
        opportunity = townhall_services.OpportunityServices.get_opportunity(id=1)
        volunteer = townhall_services.VolunteerServices.get_volunteer(id=1)

        volunteers_before = opportunity.volunteers.all()
        assert len(volunteers_before) == 0

        opportunities_before = volunteer.opportunities.all()
        assert len(opportunities_before) == 0

        townhall_services.OpportunityServices.add_volunteer_to_opportunity(1, 1)

        volunteers = opportunity.volunteers.all()
        assert len(volunteers) == 1

        opportunities = volunteer.opportunities.all()
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

        opportunities_before = volunteer.opportunities.all()
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

        opportunities = volunteer.opportunities.all()
        assert len(opportunities) == 3

    def test_add_many_volunteers_to_one_opportunity(self):
        opportunity = townhall_services.OpportunityServices.get_opportunity(id=1)
        volunteer1 = townhall_services.VolunteerServices.get_volunteer(id=1)
        volunteer2 = townhall_services.VolunteerServices.get_volunteer(id=2)
        volunteer3 = townhall_services.VolunteerServices.get_volunteer(id=3)

        volunteers_before = opportunity.volunteers.all()
        assert len(volunteers_before) == 0

        opportunties1_before = volunteer1.opportunities.all()
        assert len(opportunties1_before) == 0
        opportunties2_before = volunteer2.opportunities.all()
        assert len(opportunties2_before) == 0
        opportunties3_before = volunteer3.opportunities.all()
        assert len(opportunties3_before) == 0

        townhall_services.OpportunityServices.add_volunteer_to_opportunity(1, 1)
        townhall_services.OpportunityServices.add_volunteer_to_opportunity(1, 2)
        townhall_services.OpportunityServices.add_volunteer_to_opportunity(1, 3)

        volunteers = opportunity.volunteers.all()
        assert len(volunteers) == 3

        opportunties1 = volunteer1.opportunities.all()
        assert len(opportunties1) == 1
        opportunties2 = volunteer2.opportunities.all()
        assert len(opportunties2) == 1
        opportunties3 = volunteer3.opportunities.all()
        assert len(opportunties3) == 1

    def test_add_many_volunteers_to_many_opportunities(self):
        opportunity1 = townhall_services.OpportunityServices.get_opportunity(id=1)
        opportunity2 = townhall_services.OpportunityServices.get_opportunity(id=2)
        opportunity3 = townhall_services.OpportunityServices.get_opportunity(id=3)

        volunteer1 = townhall_services.VolunteerServices.get_volunteer(id=1)
        volunteer2 = townhall_services.VolunteerServices.get_volunteer(id=2)
        volunteer3 = townhall_services.VolunteerServices.get_volunteer(id=3)

        opportunties1_before = volunteer1.opportunities.all()
        assert len(opportunties1_before) == 0
        opportunties2_before = volunteer2.opportunities.all()
        assert len(opportunties2_before) == 0
        opportunties3_before = volunteer3.opportunities.all()
        assert len(opportunties3_before) == 0

        volunteers1_before = opportunity1.volunteers.all()
        assert len(volunteers1_before) == 0
        volunteers2_before = opportunity2.volunteers.all()
        assert len(volunteers2_before) == 0
        volunteers3_before = opportunity3.volunteers.all()
        assert len(volunteers3_before) == 0

        townhall_services.OpportunityServices.add_volunteer_to_opportunity(1, 1)
        townhall_services.OpportunityServices.add_volunteer_to_opportunity(1, 2)
        townhall_services.OpportunityServices.add_volunteer_to_opportunity(1, 3)

        townhall_services.OpportunityServices.add_volunteer_to_opportunity(2, 1)
        townhall_services.OpportunityServices.add_volunteer_to_opportunity(2, 2)

        townhall_services.OpportunityServices.add_volunteer_to_opportunity(3, 1)

        opportunties1 = volunteer1.opportunities.all()
        assert len(opportunties1) == 3
        opportunties2 = volunteer2.opportunities.all()
        assert len(opportunties2) == 2
        opportunties3 = volunteer3.opportunities.all()
        assert len(opportunties3) == 1

        volunteers1 = opportunity1.volunteers.all()
        assert len(volunteers1) == 3
        volunteers2 = opportunity2.volunteers.all()
        assert len(volunteers2) == 2
        volunteers3 = opportunity3.volunteers.all()
        assert len(volunteers3) == 1

    def test_get_all_volunteers_from_opportunity(self):
        opportunity = townhall_services.OpportunityServices.get_opportunity(id=1)
        volunteer1 = townhall_services.VolunteerServices.get_volunteer(id=1)
        volunteer2 = townhall_services.VolunteerServices.get_volunteer(id=2)
        volunteer3 = townhall_services.VolunteerServices.get_volunteer(id=3)

        volunteers_before = opportunity.volunteers.all()
        assert len(volunteers_before) == 0

        opportunties1_before = volunteer1.opportunities.all()
        assert len(opportunties1_before) == 0
        opportunties2_before = volunteer2.opportunities.all()
        assert len(opportunties2_before) == 0
        opportunties3_before = volunteer3.opportunities.all()
        assert len(opportunties3_before) == 0

        townhall_services.OpportunityServices.add_volunteer_to_opportunity(1, 1)
        townhall_services.OpportunityServices.add_volunteer_to_opportunity(1, 2)
        townhall_services.OpportunityServices.add_volunteer_to_opportunity(1, 3)

        volunteers = (
            townhall_services.OpportunityServices.get_all_volunteers_of_a_opportunity(1)
        )
        assert len(volunteers) == 3

    def test_get_all_opportunities_from_volunteer(self):
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

        opportunities_before = volunteer.opportunities.all()
        assert len(opportunities_before) == 0

        townhall_services.OpportunityServices.add_volunteer_to_opportunity(1, 1)
        townhall_services.OpportunityServices.add_volunteer_to_opportunity(2, 1)
        townhall_services.OpportunityServices.add_volunteer_to_opportunity(3, 1)

        opportunities = (
            townhall_services.OpportunityServices.get_all_opportunities_of_a_volunteer(
                1
            )
        )
        assert len(opportunities) == 3

    def test_remove_one_volunteer(self):
        opportunity = townhall_services.OpportunityServices.get_opportunity(id=1)
        volunteer1 = townhall_services.VolunteerServices.get_volunteer(id=1)
        volunteer2 = townhall_services.VolunteerServices.get_volunteer(id=2)

        volunteers_before = opportunity.volunteers.all()
        assert len(volunteers_before) == 0

        opportunties1_before = volunteer1.opportunities.all()
        assert len(opportunties1_before) == 0
        opportunties2_before = volunteer2.opportunities.all()
        assert len(opportunties2_before) == 0

        townhall_services.OpportunityServices.add_volunteer_to_opportunity(1, 1)
        townhall_services.OpportunityServices.add_volunteer_to_opportunity(1, 2)

        volunteers = opportunity.volunteers.all()
        assert len(volunteers) == 2

        opportunties1 = volunteer1.opportunities.all()
        assert len(opportunties1) == 1
        opportunties2 = volunteer2.opportunities.all()
        assert len(opportunties2) == 1

        townhall_services.OpportunityServices.remove_volunteer_from_opportunity(1, 1)

        volunteers_after = opportunity.volunteers.all()
        assert len(volunteers_after) == 1

        opportunties1_after = volunteer1.opportunities.all()
        assert len(opportunties1_after) == 0
        opportunties2_after = volunteer2.opportunities.all()
        assert len(opportunties2_after) == 1

    def test_remove_all_volunteers_from_opportunity(self):
        opportunity = townhall_services.OpportunityServices.get_opportunity(id=1)
        volunteer1 = townhall_services.VolunteerServices.get_volunteer(id=1)
        volunteer2 = townhall_services.VolunteerServices.get_volunteer(id=2)

        volunteers_before = opportunity.volunteers.all()
        assert len(volunteers_before) == 0

        opportuntities1_before = volunteer1.opportunities.all()
        assert len(opportuntities1_before) == 0
        opportuntities2_before = volunteer2.opportunities.all()
        assert len(opportuntities2_before) == 0

        townhall_services.OpportunityServices.add_volunteer_to_opportunity(1, 1)
        townhall_services.OpportunityServices.add_volunteer_to_opportunity(1, 2)

        volunteers = opportunity.volunteers.all()
        assert len(volunteers) == 2

        opportuntities1 = volunteer1.opportunities.all()
        assert len(opportuntities1) == 1
        opportuntities2 = volunteer2.opportunities.all()
        assert len(opportuntities2) == 1

        townhall_services.OpportunityServices.remove_all_volunteers_from_opportunity(1)

        volunteer_after = opportunity.volunteers.all()
        assert len(volunteer_after) == 0

        opportuntities1_after = volunteer1.opportunities.all()
        assert len(opportuntities1_after) == 0
        opportuntities2_after = volunteer2.opportunities.all()
        assert len(opportuntities2_after) == 0

    def test_remove_all_opportunities_from_volunteer(self):
        opportunity1 = townhall_services.OpportunityServices.get_opportunity(id=1)
        opportunity2 = townhall_services.OpportunityServices.get_opportunity(id=2)
        volunteer = townhall_services.VolunteerServices.get_volunteer(id=1)

        opportunities_before = volunteer.opportunities.all()
        assert len(opportunities_before) == 0

        volunteers1_before = opportunity1.volunteers.all()
        assert len(volunteers1_before) == 0
        volunteers2_before = opportunity2.volunteers.all()
        assert len(volunteers2_before) == 0

        townhall_services.OpportunityServices.add_volunteer_to_opportunity(1, 1)
        townhall_services.OpportunityServices.add_volunteer_to_opportunity(2, 1)

        opportunities = volunteer.opportunities.all()
        assert len(opportunities) == 2

        volunteers1 = opportunity1.volunteers.all()
        assert len(volunteers1) == 1
        volunteers2 = opportunity2.volunteers.all()
        assert len(volunteers2) == 1

        townhall_services.OpportunityServices.remove_all_opportunities_from_volunteer(1)

        opportunities_after = volunteer.opportunities.all()
        assert len(opportunities_after) == 0

        volunteers1_after = opportunity1.volunteers.all()
        assert len(volunteers1_after) == 0
        volunteers2_after = opportunity2.volunteers.all()
        assert len(volunteers2_after) == 0
