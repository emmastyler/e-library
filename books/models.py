from django.db import models
from django.contrib.auth.models import User

# Define UserProfile first
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

# Then define Book model
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=20)
    publication_date = models.DateField()
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default=None)
