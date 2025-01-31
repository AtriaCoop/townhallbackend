from django.test import TestCase
from myapi import models as townhall_models
from myapi import services as townhall_services

# Community

# Testing ALL tests "python manage.py test tests"
# Testing ONLY community
# python manage.py test tests.service_tests.test_community_service


class TestCommunityModel(TestCase):
    def setUp(self):
        townhall_models.Community.objects.create(
            id=1,
            name="Community1",
            description="Description1",
        )
        townhall_models.Community.objects.create(
            id=2,
            name="Community2",
            description="Description2",
        )

    def test_get_community(self):
        community = townhall_services.CommunityServices.get_community(id=1)
        self.assertIsNotNone(community)
        self.assertEqual(community.name, "Community1")
        self.assertEqual(community.description, "Description1")

    def test_get_community_not_found(self):
        community = townhall_services.CommunityServices.get_community(id=100)
        self.assertIsNone(community)

    def test_get_all_communities(self):
        community = townhall_services.CommunityServices.get_all_communities()
        self.assertEqual(len(community), 2)
        self.assertEqual(community[0].name, "Community1")
        self.assertEqual(community[0].description, "Description1")
        self.assertEqual(community[1].name, "Community2")
        self.assertEqual(community[1].description, "Description2")
