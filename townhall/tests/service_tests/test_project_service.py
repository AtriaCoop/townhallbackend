from django.test import TestCase
from myapi import models as townhall_models
from myapi import services as townhall_services
from datetime import datetime
from django.utils import timezone

# Project

# Testing ALL tests "python manage.py test tests"
# Testing ONLY project "python manage.py test tests.service_tests.test_project_service"


class TestProjectModel(TestCase):
    def setUp(self):
        townhall_models.Project.objects.create(
            id=1,
            title="Project1",
            description="Description1",
            start_date=timezone.make_aware(datetime(2024, 7, 20, 10, 0)),
            end_date=timezone.make_aware(datetime(2024, 7, 20, 20, 30)),
        )

    def test_get_project(self):
        project = townhall_services.ProjectServices.get_project(id=1)
        assert project.title == "Project1"
        assert project.description == "Description1"
        assert project.start_date == timezone.make_aware(datetime(2024, 7, 20, 10, 0))
        assert project.end_date == timezone.make_aware(datetime(2024, 7, 20, 20, 30))

    def test_get_project_not_found(self):
        project = townhall_services.ProjectServices.get_project(id=2)
        assert project is None
