from django.db import models
from django.contrib.auth.models import AbstractUser

class Student(AbstractUser):
    email = models.EmailField(unique=True)
    grade = models.IntegerField()

    def save(self, *args, **kwargs):
        if self.grade < 0 or self.grade > 12:
            raise ValueError("Grade must be between 0 and 12")
        super().save(*args, **kwargs)
