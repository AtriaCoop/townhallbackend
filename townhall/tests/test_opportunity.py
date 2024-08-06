from django.test import TestCase
from myapi import models as townhall_models
from myapi import services as townhall_services
from datetime import datetime
from django.utils import timezone

# OPPORTUNITY

# Testing ALL tests "python manage.py test myapi.tests"
# Testing ONLY opportunity "python manage.py test myapi.tests.test_opportunity"

class TestOpportunityModel(TestCase):
    def setUp(self):
        townhall_models.Opportunity.objects.create(id=1, name="Food bank", time=timezone.make_aware(datetime(2024, 7, 20, 10, 0)), description="Deliver food", location="Vancouver")
        townhall_models.Opportunity.objects.create(id=2, name="Hygiene", time=timezone.make_aware(datetime(2024, 7, 20, 10, 0)), description="Deliver clothes", location="East Vancouver")
        townhall_models.Opportunity.objects.create(id=3, name="Community Clean Up", time=timezone.make_aware(datetime(2024, 7, 20, 10, 0)), description="Clean up the neighborhood", location="West Vancouver")

    def test_get_opportunity(self):
        opportunity = townhall_services.OpportunityServices.get_opportunity(id=1)
        assert opportunity.name == "Food bank"
        assert opportunity.time == timezone.make_aware(datetime(2024, 7, 20, 10, 0))
        assert opportunity.description == "Deliver food"
        assert opportunity.location == "Vancouver"

    def test_filtered_opportunity_name_and_time(self):
        start_time = timezone.make_aware(datetime(2024, 7, 20, 0, 0))
        end_time = timezone.make_aware(datetime(2024, 7, 20, 23, 59))
        filtered_opportunity_data = townhall_services.FilteredOpportunityData(name="Food", start_time=start_time, end_time=end_time)
        opportunities = townhall_services.OpportunityServices.filtered_opportunity(filtered_opportunity_data)
        
        for o in opportunities:
            print(f"Opportunity: {o.name}, Time: {o.time}, Location: {o.location}")

        # Assert that exactly only one opportunity is returned
        assert len(opportunities) == 1

        for opportunity in opportunities:
            assert "food" in opportunity.name.lower()  # Case insensitive check
            assert start_time <= opportunity.time <= end_time  # Time range check
        

    def test_delete_opportunity(self):
        # Step 1
        test_opportunity = townhall_services.OpportunityServices.get_opportunity(id=1)
        assert test_opportunity.name == "Food bank"
        assert test_opportunity.time == timezone.make_aware(datetime(2024, 7, 20, 10, 0))
        assert test_opportunity.description == "Deliver food"
        assert test_opportunity.location == "Vancouver"

        # Step 2
        townhall_services.OpportunityServices.delete_opportunity(id=1)
        assert townhall_services.OpportunityServices.get_opportunity(id=1) is None

    def test_update_opportunity(self):
        # Step 1
        opportunity_before_update = townhall_services.OpportunityServices.get_opportunity(id=3)
        assert opportunity_before_update.name == "Community Clean Up"
        assert opportunity_before_update.time == timezone.make_aware(datetime(2024, 7, 20, 10, 0))
        assert opportunity_before_update.description == "Clean up the neighborhood"
        assert opportunity_before_update.location == "West Vancouver"
        
        # Step 2
        update_opportunity_data = townhall_services.UpdateOpportunityData(
            id = 3,
            name = "Community Gardening",
            time = timezone.make_aware(datetime(2024, 8, 15, 2, 0)),
            description = "Planting some flowers in the community center",
            location = "Richmond"
        )
        townhall_services.OpportunityServices.update_opportunity(id=3, update_opportunity_data=update_opportunity_data)

        # Step 3
        updated_opportunity = townhall_services.OpportunityServices.get_opportunity(id=3)
        assert updated_opportunity.name == "Community Gardening"
        assert updated_opportunity.time == timezone.make_aware(datetime(2024, 8, 15, 2, 0))
        assert updated_opportunity.description == "Planting some flowers in the community center"
        assert updated_opportunity.location == "Richmond"