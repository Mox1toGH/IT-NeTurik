from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Учень'),
        ('parent', 'Батько/Мати'),
        ('teacher', 'Вчитель'),
        ('director', 'Директор'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f'{self.user.username} - {self.role}'
    
class School(models.Model):
    name = models.CharField(max_length=255, unique=True)
    director = models.OneToOneField(User, on_delete=models.CASCADE, related_name="school")

    def __str__(self):
        return self.name
