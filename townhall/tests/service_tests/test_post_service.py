from django.test import TestCase
from django.core.management import call_command
from django.db.utils import IntegrityError
from myapi.models import Post, Volunteer
from myapi.services import PostServices as post_services
from myapi.types import CreatePostData
from django.utils import timezone
import os


class TestPostModel(TestCase):
    fixtures = ["volunteer_fixture.json"]

    def setUp(self):
        # Load the fixture data to set up initial state
        call_command("loaddata", "volunteer_fixture.json")

        # Get the volunteer instance from fixture
        self.volunteer = Volunteer.objects.get(pk=1)

        self.test_image_path = os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            ),  # One more dirname to go up to townhallbackend
            "image.png",
        )

    def test_create_post_with_volunteer(self):
        # Arrange: Retrieve a volunteer from the fixture
        volunteer = Volunteer.objects.get(pk=1)

        # Act: Create a new post associated with this volunteer
        post = Post.objects.create(
            volunteer=volunteer,
            content="This is a test post by Zamorak",
            created_at=timezone.now(),
        )

        # Assert: Check that post was created correctly and is linked to the volunteer
        self.assertEqual(post.volunteer, volunteer)
        self.assertEqual(post.content, "This is a test post by Zamorak")
        self.assertEqual(Post.objects.count(), 1)

    def test_post_requires_volunteer(self):
        # Act & Assert: Create a post without a volunteer and expect an IntegrityError
        with self.assertRaises(IntegrityError):
            Post.objects.create(
                content="This post should fail", created_at=timezone.now()
            )

    def test_create_post_service(self):
        post_data = CreatePostData(
            volunteer_id=self.volunteer.id,
            content="Test post content",
            created_at=timezone.now(),
            image=None,  # Optional, can be omitted
        )

        post = post_services.create_post(post_data)

        self.assertIsNotNone(post)
        self.assertEqual(post.volunteer_id, self.volunteer.id)
        self.assertEqual(post.content, "Test post content")
