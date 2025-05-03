from django.test import TestCase
from django.core.exceptions import ValidationError

from myapi.services import EventServices
from myapi.models import Event, Organization

from datetime import datetime
from django.utils import timezone


class TestEventModel(TestCase):

    def setUp(self):

        org=Organization.objects.create(
            id=1,
            name="Tester",
            location="Location",
            email="123@gmail.com",
            phone_number="123-456-7898",
            website="testsite.com",
        )

        Event.objects.create(
            id=1,
            title="event test",
            description="This is a test",
            start_time=timezone.make_aware(datetime(2025, 5, 2, 8, 0)),
            end_time=timezone.make_aware(datetime(2025, 5, 2, 15, 0)),
            location="test location",
            organization=org
        )

    def test_get_event_successful(self):
        event = EventServices.get_event(id=1)

        # checks to see if information matches actual event information
        self.assertEqual(event.title, "event test")
        self.assertEqual(event.description, "This is a test")
        self.assertEqual(event.start_time, timezone.make_aware(datetime(2025, 5, 2, 8, 0)))
        self.assertEqual(event.end_time, timezone.make_aware(datetime(2025, 5, 2, 15, 0)))
        self.assertEqual(event.location, "test location")

    def test_get_event_failure(self):

        # confirms to see if this code will give a validation error
        with self.assertRaises(ValidationError):
            EventServices.get_event(id=2)
