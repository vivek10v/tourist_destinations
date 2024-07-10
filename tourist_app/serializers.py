from rest_framework import serializers
from .models import *

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class DestinationSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    
    class Meta:
        model = Destination
        fields = '__all__'