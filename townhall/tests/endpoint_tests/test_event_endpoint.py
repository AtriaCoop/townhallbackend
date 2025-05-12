from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from myapi.models import Event, Volunteer, Organization
from django.core.files.uploadedfile import SimpleUploadedFile
import os

class EventViewSetTests(TestCase):

    def setUp(self):
        self.organization = Organization.objects.create(
            name="Test Org",
            location="Testville",
            email="test@example.com"
        )
        self.valid_payload = {
            "title": "Test Event",
            "description": "This is a test event",
            "start_time": timezone.now().isoformat(),
            "end_time": (timezone.now() + timezone.timedelta(hours=1)).isoformat(),
            "location": "UBC",
            "organization": self.organization.id
        }

    def test_create_event_success(self):
        url = reverse('event')  
        response = self.client.post(url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("event", response.data)
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(Event.objects.first().title, "Test Event")

    def test_create_event_missing_title(self):
        payload = self.valid_payload.copy()
        del payload["title"]
        url = reverse('event')
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_create_event_invalid_datetime(self):
        payload = self.valid_payload.copy()
        payload["start_time"] = "invalid-date"
        url = reverse('event')
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("start_time", response.data)

    def test_create_event_invalid_org_id(self):
        payload = self.valid_payload.copy()
        payload["organization"] = 9999  # Assuming this ID doesn't exist
        url = reverse('event')
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
