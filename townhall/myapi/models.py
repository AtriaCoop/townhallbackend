from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Volunteer(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.CharField(max_length=254)

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return self.first_name
    
    
class Opportunity(models.Model):
    name = models.CharField(max_length=100)
    time = models.DateTimeField()
    description = models.TextField()
    location = models.CharField(max_length=100)
    volunteers = models.ManyToManyField(Volunteer, related_name='volunteers', blank=True)

    def __str__(self):
        return self.name
    

class Organization(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    email = models.CharField(max_length=254)

    def __str__(self):
        return self.name
    

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.id
    

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment_id