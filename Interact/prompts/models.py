from django.db import models
from users.models import ProfileGithub

class Prompt(models.Model):
    owner = models.ForeignKey(ProfileGithub, on_delete=models.CASCADE)
    tag = models.CharField(max_length=200)
    body = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body