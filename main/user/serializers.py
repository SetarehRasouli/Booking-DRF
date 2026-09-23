from rest_framework import serializers
from django.contrib.auth.models import User
from booking.models import Provider

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields=['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ProviderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Provider
        fields=['name', 'email', 'start_time', 'end_time']

    def validate(self, data):
        user = self.context['request'].user
        if Provider.objects.filter(user=user).exists():
            raise serializers.ValidationError("This provider already exist")
        return data


    def create(self, validated_data):
        user = self.context['request'].user
        provider = Provider.objects.create(user=user, **validated_data)
        return provider

    


