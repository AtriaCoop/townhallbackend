from django.test import TestCase
from myapi import models as townhall_models
from myapi import services as townhall_services
from datetime import datetime
from django.utils import timezone
from myapi.types import CreateProjectData
from myapi.services import ProjectServices

# Project

# Testing ALL tests "python manage.py test tests"
# Testing ONLY project python manage.py test tests.service_tests.test_project_service


class TestProjectModel(TestCase):
    def setUp(self):
        self.community = townhall_models.Community.objects.create(
            id=1, name="Community1", description="Description1"
        )
        townhall_models.Project.objects.create(
            id=1,
            title="Project1",
            description="Description1",
            start_date=timezone.make_aware(datetime(2024, 7, 20, 10, 0)),
            end_date=timezone.make_aware(datetime(2024, 7, 20, 20, 30)),
            community=self.community,
        )
        townhall_models.Project.objects.create(
            id=2,
            title="Project2",
            description="Description2",
            start_date=timezone.make_aware(datetime(2024, 7, 20, 10, 0)),
            end_date=timezone.make_aware(datetime(2024, 7, 20, 20, 30)),
            community=self.community,
        )
        self.project_data = CreateProjectData(
            id=3,
            title="Project3",
            description="Description3",
            start_date=timezone.make_aware(datetime(2024, 7, 20, 10, 0)),
            end_date=timezone.make_aware(datetime(2024, 7, 20, 20, 30)),
            community=self.community,
        )

    def test_get_project(self):
        project = townhall_services.ProjectServices.get_project(id=1)
        self.assertIsNotNone(project)
        self.assertEqual(project.title, "Project1")
        self.assertEqual(project.description, "Description1")
        self.assertEqual(
            project.start_date, timezone.make_aware(datetime(2024, 7, 20, 10, 0))
        )
        self.assertEqual(
            project.end_date, timezone.make_aware(datetime(2024, 7, 20, 20, 30))
        )
        self.assertEqual(project.community, self.community)

    def test_get_project_not_found(self):
        project = townhall_services.ProjectServices.get_project(id=100)
        self.assertIsNone(project)

    def test_get_all_projects(self):
        projects = townhall_services.ProjectServices.get_all_projects()
        self.assertEqual(len(projects), 2)
        self.assertEqual(projects[0].title, "Project1")
        self.assertEqual(projects[1].title, "Project2")

    def test_get_all_projects_empty(self):
        townhall_models.Project.objects.all().delete()
        projects = townhall_services.ProjectServices.get_all_projects()
        self.assertEqual(len(projects), 0)

    def test_create_project_service(self):
        project = ProjectServices.create_project(self.project_data)

        self.assertEqual(project.id, 3)
        self.assertEqual(project.title, "Project3")
        self.assertEqual(project.community, self.community)
