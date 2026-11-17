from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('trainer', 'Trainer/Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def is_student(self):
        return self.role == 'student'

    def is_trainer(self):
        return self.role == 'trainer' or self.is_superuser