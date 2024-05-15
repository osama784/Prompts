from rest_framework import serializers

from .models import Prompt
from users.serializers import ProfileSerializer

class PromptSerializer(serializers.ModelSerializer):
    # user = ProfileSerializer(source='owner', read_only=True)
    # owner = serializers.IntegerField(write_only=True)

    class Meta:
        model = Prompt
        fields = '__all__'
         

    # def to_representation(self, instance):
    #     data = PromptSerializerShow(instance).data
    #     return super().to_representation(instance)

    # def update(self, instance, validated_data):
    #     request = self.context.get('request')
    #     instance.owner = request.user.profile
    #     return instance    


class PromptSerializerShow(serializers.ModelSerializer):
    owner = ProfileSerializer()
    class Meta:
        model = Prompt
        fields = [
            'id',
            'owner',
            'name',
            'message',
            'created'
        ]

class PromptSerializerShowRestricted(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Prompt
        fields = [
            'id',
            'owner_username',
            'name',
            'message',
            'created'
        ]                


    


