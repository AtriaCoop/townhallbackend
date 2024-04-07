from django.db import models

# Create your models here.

class Volunteer(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    age = models.IntegerField()

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)


    def __str__(self):
        return self.first_name