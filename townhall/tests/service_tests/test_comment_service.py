from django.test import TestCase
from myapi import models as townhall_models

# from myapi.models import Comment
from datetime import datetime

# COMMENT


# I tried to copy the test_opportunity_service.py file.
# I am not sure if this is the correct way.
class TestCommentModel(TestCase):
    def setUp(self):
        townhall_models.Comment.objects.create(
            commend_id=1,
            user_id=1,
            post_id=1,
            content="Testing",
            created_at=datetime(2024, 7, 20, 10, 0),
        )
