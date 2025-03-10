from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from myapi import models as townhall_models
from datetime import datetime
from django.core.exceptions import ValidationError


class TestEndpointComment(TestCase):

    def setUp(self):
        self.client = APIClient()
        townhall_models.Comment.objects.create(
            id=1,
            user_id=1,
            post_id=1,
            content="Testing",
            created_at=datetime(2024, 7, 20, 10, 0),
        )
        townhall_models.Comment.objects.create(
            id=10,
            user_id=10,
            post_id=10,
            content="Epic volunteering",
            created_at=datetime(2025, 1, 1, 10, 0),
        )

    def test_create_comment_success(self):
        self.url = "comment/"
        valid_data = {
            "user_id": "1",
            "post_id": "1",
            "content": "Some comment",
        }

        response = self.client.post(self.url, valid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Comment Created Successfully")

    def test_create_comment_fail_invalid_data(self):
        self.url = "comment/"
        invalid_data = {
            "user_id": "1",
            "post_id": "1",
            # invalid because missing content
        }

        response = self.client.post(self.url, invalid_data, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_comment_fail_service_error(self, mock_create_comment):
        mock_create_comment.side_effect = ValidationError("random message")
        self.url = "comment/"
        valid_data = {
            "user_id": "1",
            "post_id": "1",
            "content": "Some comment",
        }

        # Act
        response = self.client.post(self.url, valid_data, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "['random message']")
