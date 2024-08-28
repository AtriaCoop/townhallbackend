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
        townhall_models.Opportunity.objects.create(id=1, title="Food bank", description="Deliver food", start_time=timezone.make_aware(datetime(2024, 7, 20, 10, 0)), end_time=timezone.make_aware(datetime(2024, 7, 20, 20, 30)), location="Vancouver")
        townhall_models.Opportunity.objects.create(id=2, title="Hygiene", description="Deliver clothes", start_time=timezone.make_aware(datetime(2024, 7, 20, 10, 0)), end_time=timezone.make_aware(datetime(2024, 7, 20, 21, 45)), location="East Vancouver")
        townhall_models.Opportunity.objects.create(id=3, title="Community Clean Up", description="Clean up the neighborhood", start_time=timezone.make_aware(datetime(2024, 7, 20, 10, 0)), end_time=timezone.make_aware(datetime(2024, 7, 20, 21, 15)), location="West Vancouver")

    def test_get_opportunity(self):
        opportunity = townhall_services.OpportunityServices.get_opportunity(id=1)
        assert opportunity.title == "Food bank"
        assert opportunity.description == "Deliver food"
        assert opportunity.start_time == timezone.make_aware(datetime(2024, 7, 20, 10, 0))
        assert opportunity.end_time == timezone.make_aware(datetime(2024, 7, 20, 20, 30))
        assert opportunity.location == "Vancouver"

    def test_filtered_opportunity_name_and_time(self):
        starting_start_time = timezone.make_aware(datetime(2024, 7, 20, 0, 0))
        starting_end_time = timezone.make_aware(datetime(2024, 7, 20, 23, 59))
        filtered_opportunity_data = townhall_services.FilteredOpportunityData(title="Food", starting_start_time=starting_start_time, starting_end_time=starting_end_time)
        opportunities = townhall_services.OpportunityServices.filtered_opportunity(filtered_opportunity_data)
        
        for o in opportunities:
            print(f"Opportunity: {o.title}, Start Time: {o.start_time}, Location: {o.location}")

        # Assert that exactly only one opportunity is returned
        assert len(opportunities) == 1

        for opportunity in opportunities:
            assert "food" in opportunity.title.lower()  # Case insensitive check
            assert starting_start_time <= opportunity.start_time <= starting_end_time  # Time range check
        

    def test_delete_opportunity(self):
        # Step 1
        opportunity = townhall_services.OpportunityServices.get_opportunity(id=1)
        assert opportunity.title == "Food bank"
        assert opportunity.description == "Deliver food"
        assert opportunity.start_time == timezone.make_aware(datetime(2024, 7, 20, 10, 0))
        assert opportunity.end_time == timezone.make_aware(datetime(2024, 7, 20, 20, 30))
        assert opportunity.location == "Vancouver"

        # Step 2
        townhall_services.OpportunityServices.delete_opportunity(id=1)
        assert townhall_services.OpportunityServices.get_opportunity(id=1) is None

    def test_update_opportunity(self):
        # Step 1
        opportunity_before_update = townhall_services.OpportunityServices.get_opportunity(id=3)
        assert opportunity_before_update.title == "Community Clean Up"
        assert opportunity_before_update.description == "Clean up the neighborhood"
        assert opportunity_before_update.start_time == timezone.make_aware(datetime(2024, 7, 20, 10, 0))
        assert opportunity_before_update.end_time == timezone.make_aware(datetime(2024, 7, 20, 21, 15))
        assert opportunity_before_update.location == "West Vancouver"
        
        # Step 2
        update_opportunity_data = townhall_services.UpdateOpportunityData(
            id = 3,
            title = "Community Gardening",
            description = "Planting some flowers in the community center",
            start_time = timezone.make_aware(datetime(2024, 8, 15, 2, 0)),
            end_time = timezone.make_aware(datetime(2024, 8, 15, 10, 30)),
            location = "Richmond"
        )
        townhall_services.OpportunityServices.update_opportunity(id=3, update_opportunity_data=update_opportunity_data)

        # Step 3
        updated_opportunity = townhall_services.OpportunityServices.get_opportunity(id=3)
        assert updated_opportunity.title == "Community Gardening"
        assert updated_opportunity.description == "Planting some flowers in the community center"
        assert updated_opportunity.start_time == timezone.make_aware(datetime(2024, 8, 15, 2, 0))
        assert updated_opportunity.end_time == timezone.make_aware(datetime(2024, 8, 15, 10, 30))
        assert updated_opportunity.location == "Richmond"