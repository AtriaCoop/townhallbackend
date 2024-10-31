import pytest
from rest_framework import status
from rest_framework.test import APIClient
from myapi import models as townhall_models


@pytest.mark.django_db  # Enables access to database
class TestEndpointOrganization:

    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def setup(self):
        townhall_models.Organization.objects.create(
            id=1,
            name="Sample Organization",
            location="Sample Location",
            email="Sample Email",
            phone_number="Sample Phone Number",
            website="Sample Website",
        )

    # GET Organization
    def test_get_organization(self, api_client, setup):
        url = "/organization/"
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]["name"] == "Sample Organization"
        assert response.data[0]["location"] == "Sample Location"
        assert response.data[0]["email"] == "Sample Email"
        assert response.data[0]["phone_number"] == "Sample Phone Number"
        assert response.data[0]["website"] == "Sample Website"

    # UPDATE Organization
    def test_put_organization(self, api_client, setup):
        url = "/organization/?id=1"
        update_data = {
            "name": "Updated Organization",
            "location": "Updated Location",
            "email": "updated_organization@example.com",
            "phone_number": "604-111-111",
            "website": "https://updated-website.com",
        }
        response = api_client.put(url, update_data)
        print(response.data)

        assert response.status_code == status.HTTP_200_OK
        # Confirm data has been updated
        updated_organization = townhall_models.Organization.objects.get(id=1)
        assert updated_organization.name == "Updated Organization"
        assert updated_organization.location == "Updated Location"
        assert updated_organization.email == "updated_organization@example.com"
        assert updated_organization.phone_number == "604-111-111"
        assert updated_organization.website == "https://updated-website.com"

    # DELETE Organization
    def test_delete_organization(self, api_client, setup):
        # First, make sure the organization exists before deleting it
        url = "/organization/?id=1"
        response = api_client.get(url)
        assert (
            response.status_code == status.HTTP_200_OK
        )  # Ensure the organization exists

        # Now, delete the organization
        response = api_client.delete(url)
        assert (
            response.status_code == status.HTTP_204_NO_CONTENT
        )  # Ensure successful deletion

        # Verify the organization has been deleted by attempting to GET it again
        response = api_client.get(url)
        assert (
            response.status_code == status.HTTP_404_NOT_FOUND
        )  # Ensure it's no longer available
