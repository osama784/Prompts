from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Profile, ProfileGithub

from . import validators


class ProfileSerializer(serializers.ModelSerializer):
    prompts_url = serializers.HyperlinkedIdentityField(
        view_name='profile-prompts',
        lookup_field= 'username'
    )
    # username = serializers.CharField(validators=[validators.unique_name])

    class Meta:
        model = Profile
        fields = [
            'id',
            'prompts_url',
            'username',
            # 'owner',
            'email',
            'social_facebook',
            'social_github',
            'created',
        ]


class ProfileGithubSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[validators.unique_email])
    class Meta:
        model = ProfileGithub
        fields = '__all__'