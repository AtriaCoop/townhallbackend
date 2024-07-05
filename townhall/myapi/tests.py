from django.test import TestCase
from myapi import models as townhall_models
from myapi import services as townhall_services

# Run test class with "python manage.py test"

class TownhallTestCase(TestCase):
    def setUp(self):
        townhall_models.Volunteer.objects.create(id=1, first_name="Zamorak", last_name="Red", age=11)
        townhall_models.Volunteer.objects.create(id=2, first_name="Guthix", last_name="Green", age=77)

    def test_get_volunteer(self):
        volunteer_1 = townhall_services.VolunteerServices.get_volunteer(id=1)
        assert volunteer_1.first_name == "Zamorak"
        assert volunteer_1.last_name == "Red"
        assert volunteer_1.age == 11

    def test_dummy_test(self):
        pass