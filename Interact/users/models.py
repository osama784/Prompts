from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)
    social_facebook = models.URLField(null=True, blank=True)
    social_github = models.URLField(null=True, blank=True)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class ProfileGithub(models.Model):
    username = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    image = models.URLField()

    def __str__(self):
        return self.username
