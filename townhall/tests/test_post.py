from django.test import TestCase
from django.core.management import call_command
from django.db.utils import IntegrityError
from myapi.models import Post, Volunteer
from django.utils import timezone

class TestPostModel(TestCase):
    fixtures = ['volunteer_fixture.json']

    def setUp(self):
        # Load the fixture data to set up initial state
        call_command('loaddata', 'volunteer_fixture.json')

    def test_create_post_with_volunteer(self):
        # Arrange: Retrieve a volunteer from the fixture
        volunteer = Volunteer.objects.get(pk=1)

        # Act: Create a new post associated with this volunteer
        post = Post.objects.create(
            volunteer=volunteer,
            content="This is a test post by Zamorak",
            created_at=timezone.now()
        )

        # Assert: Check that the post was created correctly and is linked to the volunteer
        self.assertEqual(post.volunteer, volunteer)
        self.assertEqual(post.content, "This is a test post by Zamorak")
        self.assertEqual(Post.objects.count(), 1)

    def test_post_requires_volunteer(self):
        # Act & Assert: Try to create a post without a volunteer and expect an IntegrityError
        with self.assertRaises(IntegrityError):
            Post.objects.create(
                content="This post should fail",
                created_at=timezone.now()
            )
