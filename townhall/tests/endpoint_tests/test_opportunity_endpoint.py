import pytest
from rest_framework import status
from rest_framework.test import APIClient
from myapi import models as townhall_models
from datetime import datetime
from django.utils import timezone


@pytest.mark.django_db  # Enables access to database
class TestEndpointOpportunity:

    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def setup(self):
        townhall_models.Opportunity.objects.create(
            id=1,
            title="Sample Opportunity",
            start_time=timezone.make_aware(datetime(2024, 7, 20, 10, 0)),
            end_time=timezone.make_aware(datetime(2024, 7, 20, 10, 0)),
            description="Sample description",
            location="Sample location",
        )

    # GET Opportunity
    def test_get_opportunity(self, api_client, setup):
        url = "/opportunity/"
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]["title"] == "Sample Opportunity"
        assert response.data[0]["description"] == "Sample description"
        assert response.data[0]["location"] == "Sample location"
        assert response.data[0]["start_time"] == "2024-07-20T10:00:00Z"
        assert response.data[0]["end_time"] == "2024-07-20T10:00:00Z"

    # UPDATE Opportunity
    def test_put_opportunity(self, api_client, setup):
        url = "/opportunity/?id=1"
        update_data = {
            "title": "Updated Opportunity",
            "start_time": timezone.make_aware(datetime(2024, 8, 20, 12, 0)),
            "end_time": timezone.make_aware(datetime(2024, 8, 20, 12, 0)),
            "description": "Updated description",
            "location": "Updated location",
        }
        response = api_client.put(url, update_data)

        assert response.status_code == status.HTTP_200_OK
        # Confirm data has been updated
        updated_opportunity = townhall_models.Opportunity.objects.get(id=1)
        assert updated_opportunity.title == "Updated Opportunity"
        assert updated_opportunity.description == "Updated description"
        assert updated_opportunity.location == "Updated location"
        assert updated_opportunity.start_time == timezone.make_aware(
            datetime(2024, 8, 20, 12, 0)
        )
        assert updated_opportunity.end_time == timezone.make_aware(
            datetime(2024, 8, 20, 12, 0)
        )

    # DELETE Opportunity
    def test_delete_opportunity(self, api_client, setup):
        # First, make sure the opportunity exists before deleting it
        url = "/opportunity/?id=1"
        response = api_client.get(url)
        assert (
            response.status_code == status.HTTP_200_OK
        )  # Ensure the opportunity exists

        # Now, delete the opportunity
        response = api_client.delete(url)
        assert (
            response.status_code == status.HTTP_204_NO_CONTENT
        )  # Ensure successful deletion

        # Verify the opportunity has been deleted by attempting to GET it again
        response = api_client.get(url)
        assert (
            response.status_code == status.HTTP_404_NOT_FOUND
        )  # Ensure it's no longer available
