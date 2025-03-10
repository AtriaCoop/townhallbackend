from django.test import TestCase
from datetime import datetime
from django.utils import timezone
from myapi.services import CommentServices
from myapi import models as townhall_models

# from myapi import services as townhall_services
from myapi.types import CreateCommentData
from myapi.models import Comment, Post


class TestCommentModel(TestCase):
    def setUp(self):
        # Start with a clean database
        Comment.objects.all().delete()
        # Post.objects.all().delete()
        # Volunteer.objects.all().delete()

        volunteer = townhall_models.Volunteer.objects.create(
            id=1,
            first_name="Zamorak",
            last_name="Red",
            gender="M",
            email="zamorak.red@gmail.com",
        )

        self.post = Post.objects.create(
            volunteer=volunteer,
            content="This is a test post by Gen",
            created_at=timezone.make_aware(datetime(2024, 7, 19, 10, 0)),
        )

        # Comment data
        self.comment_data = CreateCommentData(
            id=1,
            user_id=1,  # Use the volunteer's ID
            post_id=self.post.id,
            content="Testing",
            created_at=timezone.make_aware(datetime(2024, 7, 20, 10, 0)),
        )

    def test_create_comment(self):
        # Call the service function
        comment = CommentServices.create_comment(self.comment_data)

        # Refresh the comment from the database
        comment_from_db = Comment.objects.get(id=comment.id)

        # Assertions
        self.assertIsInstance(comment, Comment)
        self.assertEqual(comment_from_db.user_id, 1)
        self.assertEqual(comment_from_db.post_id, self.post.id)
        self.assertEqual(comment_from_db.content, "Testing")
        self.assertEqual(
            comment_from_db.created_at,
            timezone.make_aware(datetime(2024, 7, 20, 10, 0)),
        )
