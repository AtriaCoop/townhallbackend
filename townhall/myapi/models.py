from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# Create your models here.

class Volunteer(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=128, default=make_password('default_password'))
    is_active = models.BooleanField(default=True)

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return self.first_name
    
    def save(self, *args, **kwargs):
        # Ensure the password is hashed before saving
        if not self.password.startswith('pbkdf2_sha256'):
            self.password = make_password(self.password)
        super(Volunteer, self).save(*args, **kwargs)
    
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
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=100)
    website = models.URLField(max_length=100)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id)
    
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id)
