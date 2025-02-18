from django.test import TestCase
from django.utils import timezone
from django.db.utils import IntegrityError
from myapi.models import Post, Volunteer
from myapi.dao import PostDao  # Import the PostDao class
from myapi.types import CreatePostData  # Import CreatePostData


class PostDaoTests(TestCase):
    fixtures = ["volunteer_fixture.json"]  # Optional: If you have fixture data, use it

    def setUp(self):
        # You can set up your test data here. This will be run before each test.
        self.volunteer = Volunteer.objects.create(
            id=1,  # Example volunteer ID, adjust as necessary
            # Populate other fields as needed, e.g., name, email, etc.
        )

    def test_create_post_with_volunteer(self):
        # Arrange: Create post data with the volunteer
        post_data = CreatePostData(
            id=1,  # Or any unique ID for your post
            user_id=self.volunteer.id,
            content="This is a test post",
            created_at=timezone.now(),
        )

        # Act: Use PostDao to create a new post associated with this volunteer
        post = PostDao.create_post(post_data)

        # Assert: Check if post was created correctly and is linked to the volunteer
        self.assertEqual(post.volunteer, self.volunteer)
        self.assertEqual(post.content, "This is a test post")
        self.assertEqual(Post.objects.count(), 1)

    def test_post_requires_volunteer(self):
        # Act & Assert: Create post data without volunteer and expect an IntegrityError
        post_data = CreatePostData(
            id=1,
            user_id=None,  # No volunteer assigned
            content="This post should fail",
            created_at=timezone.now(),
        )

        # Act & Assert: Expect IntegrityError when creating a post without a volunteer
        with self.assertRaises(IntegrityError):
            PostDao.create_post(post_data)
