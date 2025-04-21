from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from myapi.models import Post, Volunteer
from django.core.files.uploadedfile import SimpleUploadedFile
import os


class PostViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a test volunteer
        self.volunteer = Volunteer.objects.create(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password="testpass123",
            gender="M",
        )

        # Read the actual image file from project root
        self.test_image_path = os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            ),  # One more dirname to go up to townhallbackend
            "image.png",
        )

        # Read the image content
        with open(self.test_image_path, "rb") as img:
            self.image_content = img.read()

        # Test post data with real image
        self.valid_post_data = {
            "volunteer": self.volunteer.id,
            "content": "Test post content",
            "image": SimpleUploadedFile(
                name="test.png", content=self.image_content, content_type="image/png"
            ),
        }

        self.invalid_post_data = {
            "volunteer": self.volunteer.id,
            "content": "",  # Empty content
        }

        self.url = "/post/"  # Removed leading slash

    def test_create_post_success(self):
        """Test creating a post with valid data"""
        # Create fresh file for each test to avoid file pointer issues
        test_file = SimpleUploadedFile(
            name="test.png", content=self.image_content, content_type="image/png"
        )

        data = {
            "volunteer": self.volunteer.id,
            "content": "Test post content",
            "image": test_file,
        }

        response = self.client.post(self.url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(response.data["message"], "Post Created Successfully")
        self.assertEqual(response.data["post"]["content"], data["content"])

    def test_create_post_invalid_data(self):
        """Test creating a post with invalid data"""
        response = self.client.post(
            self.url, self.invalid_post_data, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 0)

    def test_create_post_nonexistent_volunteer(self):
        """Test creating a post with a nonexistent volunteer"""
        self.valid_post_data["volunteer"] = 999  # Non-existent volunteer ID
        response = self.client.post(self.url, self.valid_post_data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
