from rest_framework.validators import UniqueValidator
from .models import Profile, ProfileGithub


unique_email = UniqueValidator(ProfileGithub.objects.all(), lookup='iexact')