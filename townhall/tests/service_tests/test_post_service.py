from django.test import TestCase
from django.core.management import call_command
from django.db.utils import IntegrityError
from myapi.models import Post, Volunteer
from myapi.services import PostServices
from myapi.types import CreatePostData
from django.utils import timezone
from datetime import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
import os


class TestPostModel(TestCase):
    fixtures = ["volunteer_fixture.json"]

    def setUp(self):
        # Load the fixture data to set up initial state
        call_command("loaddata", "volunteer_fixture.json")

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
        # Arrange: Retrieve a volunteer from the fixture
        volunteer = Volunteer.objects.get(pk=1)

        with open(self.test_image_path, "rb") as f:
            image = SimpleUploadedFile(
                name="image.png", content=f.read(), content_type="image/png"
            )

        # Create a CreatePostData instance with test data
        post_data = CreatePostData(
            id=1,
            user_id=volunteer.id,
            content="This is a test post via service",
            created_at=datetime.now(),
            image=image,
        )

        # Act: Use the PostServices to create a post
        post = PostServices.create_post(post_data)

        # Assert: Check that post was created correctly and is linked to the volunteer
        self.assertEqual(post.volunteer.id, volunteer.id)
        self.assertEqual(post.content, "This is a test post via service")
        self.assertEqual(Post.objects.count(), 1)
        self.assertTrue(post.image)
        self.assertTrue(os.path.exists(post.image.path))
