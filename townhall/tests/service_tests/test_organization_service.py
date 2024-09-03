from django.test import TestCase
from myapi import models as townhall_models
from myapi import services as townhall_services

# ORGANIZATION

# Testing ALL tests "python manage.py test tests"
# Testing ONLY organization "python manage.py test tests.test_organization"


class TestOrganizationModel(TestCase):
    def setUp(self):
        townhall_models.Organization.objects.create(
            id=1,
            name="Goodwill",
            location="Victoria",
            email="goodwill@gmail.com",
            phone_number="778-123-4567",
            website="goodwill.ca",
        )
        townhall_models.Organization.objects.create(
            id=2,
            name="Salvation Army",
            location="Richmond",
            email="salvationarmy@hotmail.ca",
            phone_number="604-987-6543",
            website="salvationarmy.com",
        )

    def test_get_organization(self):
        organization = townhall_services.OrganizationServices.get_organization(id=1)
        assert organization.name == "Goodwill"
        assert organization.location == "Victoria"
        assert organization.email == "goodwill@gmail.com"
        assert organization.phone_number == "778-123-4567"
        assert organization.website == "goodwill.ca"

    def test_update_organization(self):
        organization_before_update = (
            townhall_services.OrganizationServices.get_organization(id=2)
        )
        assert organization_before_update.name == "Salvation Army"
        assert organization_before_update.location == "Richmond"
        assert organization_before_update.email == "salvationarmy@hotmail.ca"
        assert organization_before_update.phone_number == "604-987-6543"
        assert organization_before_update.website == "salvationarmy.com"

        update_organization_data = townhall_services.UpdateOrganizationData(
            id=2,
            name="Talize",
            location="Vancouver",
            email="salvationarmy2024@hotmail.ca",
            phone_number="123-456-7890",
            website="salvationarmy2024.com",
        )
        townhall_services.OrganizationServices.update_organization(
            update_organization_data
        )

        updated_organization = townhall_services.OrganizationServices.get_organization(
            id=2
        )
        assert updated_organization.name == "Talize"
        assert updated_organization.location == "Vancouver"
        assert updated_organization.email == "salvationarmy2024@hotmail.ca"
        assert updated_organization.phone_number == "123-456-7890"
        assert updated_organization.website == "salvationarmy2024.com"

    def test_delete_organization(self):
        # Step 1
        organization = townhall_services.OrganizationServices.get_organization(id=1)
        assert organization.name == "Goodwill"
        assert organization.location == "Victoria"
        assert organization.email == "goodwill@gmail.com"
        assert organization.phone_number == "778-123-4567"
        assert organization.website == "goodwill.ca"

        # Step 2
        townhall_services.OrganizationServices.delete_organization(id=1)
        assert townhall_services.OrganizationServices.get_organization(id=1) is None

    def test_filtered_organization_name_and_location(self):
        filtered_organization_data = townhall_services.FilteredOrganizationData(
            name="Goodwill", location="Victoria"
        )
        organizations = townhall_services.OrganizationServices.filtered_organization(
            filtered_organization_data
        )

        for o in organizations:
            print(f"Organization: {o.name}, Location: {o.location}")

        # Assert that exactly only one opportunity is returned
        assert len(organizations) == 1

        for organization in organizations:
            assert "goodwill" in organization.name.lower()  # Case insensitive check
            assert "victoria" in organization.location.lower()
