from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Volunteer(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(
        max_length=128, default=make_password("default_password")
    )
    is_active = models.BooleanField(default=True)

    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.first_name

    def save(self, *args, **kwargs):
        # Ensure the password is hashed before saving
        if not self.password.startswith("pbkdf2_sha256"):
            self.password = make_password(self.password)
        super(Volunteer, self).save(*args, **kwargs)


class Opportunity(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=100)
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE)
    volunteers = models.ManyToManyField(
        Volunteer, related_name="opportunities", blank=True
    )

    def __str__(self):
        return self.title


class Organization(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=100)
    website = models.URLField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to="post_images/", null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id)


class Task(models.Model):
    """
    Model representing a task in the system with fields for name, description, deadline,
    status, and relationships to volunteers and organizations.
    """

    class TaskStatus(models.TextChoices):
        OPEN = "open", _("Open")
        IN_PROGRESS = "in_progress", _("In Progress")
        COMPLETED = "completed", _("Completed")

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.OPEN,
    )
    assigned_to = models.ForeignKey(
        "Volunteer", on_delete=models.SET_NULL, null=True, related_name="assigned_tasks"
    )
    created_by = models.ForeignKey(
        "Volunteer", on_delete=models.SET_NULL, null=True, related_name="created_tasks"
    )
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Chat(models.Model):
    participants = models.ManyToManyField(User, related_name="chats")
    started_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.participants


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=100)
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    # community_id = models.ForeignKey(Community, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
