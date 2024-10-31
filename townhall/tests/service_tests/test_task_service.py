from django.test import TestCase
from django.core.management import call_command
from django.utils import timezone
from datetime import datetime
from myapi.services import TaskServices
from myapi.types import CreateTaskData, UpdateTaskData
from myapi.models import Task, Volunteer, Organization


class TaskServiceTests(TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Load fixtures and set up test data before running tests.
        """
        super().setUpClass()
        # Load the volunteer fixture
        call_command("loaddata", "volunteer_fixture.json")
        call_command("loaddata", "organization_fixture.json")
        call_command("loaddata", "task_fixture.json")

    def setUp(self):
        """
        Arrange: Set up necessary objects for the tests.
        """
        # Clear all tasks to ensure the test starts with a clean database
        Task.objects.all().delete()

        self.volunteer = Volunteer.objects.get(pk=1)
        self.organization = Organization.objects.create(
            name="Test Organization",
            location="Test Location",
            email="testorg@example.com",
        )

        self.task_data = CreateTaskData(
            name="Test Task",
            description="Task description",
            deadline=timezone.make_aware(datetime(2024, 12, 31, 23, 59, 59)),
            status=Task.TaskStatus.OPEN,
            assigned_to=self.volunteer.id,
            created_by=self.volunteer.id,
            organization_id=self.organization.id,
        )

    def test_create_task(self):
        """
        Test creating a task using TaskServices.
        """
        # Act: Call the create_task service method with the initial task data
        task = TaskServices.create_task(self.task_data)

        # Assert: Verify that the task is created correctly with the expected values
        self.assertEqual(task.name, "Test Task")
        self.assertEqual(task.assigned_to, self.volunteer)
        self.assertEqual(task.status, Task.TaskStatus.OPEN)

    def test_get_all_tasks(self):
        """
        Test retrieving all tasks using TaskServices.
        """
        # Arrange: Ensure there are no tasks before we start
        Task.objects.all().delete()

        # Act: Create a task and retrieve all tasks
        TaskServices.create_task(self.task_data)
        tasks = TaskServices.get_all_tasks()

        # Debugging: Print the names of all tasks (for debugging purposes)
        for task in tasks:
            print(f"Task name: {task.name}")

        # Assert: Verify that the task list contains exactly one task
        self.assertEqual(len(tasks), 1)  # Expecting only 1 task to be present
        self.assertEqual(tasks[0].name, "Test Task")
        self.assertEqual(tasks[0].status, Task.TaskStatus.OPEN)

    def test_get_task_by_id(self):
        """
        Test retrieving a task by ID using TaskServices.
        """
        # Arrange: Create a task and get its ID
        task = TaskServices.create_task(self.task_data)

        # Act: Use the service to get the task by its ID
        retrieved_task = TaskServices.get_task_by_id(task.id)

        # Assert: Verify that the retrieved task matches the created task
        self.assertEqual(retrieved_task.name, "Test Task")
        self.assertEqual(retrieved_task.status, Task.TaskStatus.OPEN)

    def test_update_task(self):
        """
        Test updating a task using TaskServices.
        """
        # Arrange: Create a task and prepare update data
        task = TaskServices.create_task(self.task_data)
        update_data = UpdateTaskData(
            id=task.id, name="Updated Task", status=Task.TaskStatus.IN_PROGRESS
        )

        # Act: Call the update_task service method
        updated_task = TaskServices.update_task(task.id, update_data)

        # Assert: Verify that the task is updated with the new values
        self.assertEqual(updated_task.name, "Updated Task")
        self.assertEqual(updated_task.status, Task.TaskStatus.IN_PROGRESS)

    def test_delete_task(self):
        """
        Test deleting a task using TaskServices.
        """
        # Arrange: Create a task and get its ID
        task = TaskServices.create_task(self.task_data)

        # Act: Call the delete_task service method
        TaskServices.delete_task(task.id)

        # Act: Try to retrieve the task by its ID after deletion
        retrieved_task = TaskServices.get_task_by_id(task.id)

        # Assert: Verify that the task is no longer found (i.e., it is deleted)
        self.assertIsNone(retrieved_task)
