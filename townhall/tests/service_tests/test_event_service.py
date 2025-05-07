from django.test import TestCase

from myapi.services import EventServices
from myapi.models import Organization

from django.utils import timezone

from myapi.types import CreateEventData


class TestEventModel(TestCase):

    def setUp(self):

        self.organization = Organization.objects.create(
            name="Test Organization",
            location="Test Location",
            email="testorg@example.com",
        )

        self.event_data = CreateEventData(
            title="Title",
            description="This is a test",
            start_time=timezone.now(),
            end_time=timezone.now(),
            location="UBC",
            organization=self.organization,
        )

    def test_create_event_service(self):

        event = EventServices.create_event(self.event_data)

        self.assertEqual(event.title, "Title")
        self.assertEqual(event.description, "This is a test")
        self.assertEqual(event.organization, self.organization)
