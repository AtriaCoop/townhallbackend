import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from myapi import models as townhall_models

@pytest.mark.django_db 
class TestEndpointVolunteer:

    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def setup(self):
        townhall_models.Volunteer.objects.create(
            id = 1,
            first_name = "John",
            last_name = "Doe",
            email = "Johndoe@townhall.com",
        )

    # GET Voluinteer
    def test_get_volunteer(self, api_client, setup):
        url = '/volunteer/?id=1'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['first_name'] == "John"
        assert response.data['last_name'] == "Doe"
        assert response.data['email'] == "Johndoe@townhall.com"