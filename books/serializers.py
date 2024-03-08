from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'  # Serialize all fields of the Book model

# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User

class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        # Check if username or email already exist
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username already exists')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already exists')

        return data
