from django.contrib.auth.models import User
from rest_framework import serializers
from .models import TravelHistory, CustomUser
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'last_name', 'email', 'password', 'confirm_password', 'phone']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.pop('confirm_password', None)

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")

        email = data.get('email')
        if email:
            try:
                validate_email(email)
            except ValidationError:
                raise serializers.ValidationError("Invalid email address")

            if CustomUser.objects.filter(email=email).exists():
                raise serializers.ValidationError("This email is already in use.")

        phone_number = data.get('phone')
        if phone_number:
            if not phone_number.isdigit() or len(phone_number) != 10:
                raise serializers.ValidationError("Invalid phone number. Please enter a 10-digit number.")

        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(**validated_data, password=password)
        return user


class TravelHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelHistory
        fields = ["id", "location", "destination", "created_at", "logged_user"]
        extra_kwargs = {'logged_user': {'write_only': True}}


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            # Modify the authenticate function call to use email as username
            user = authenticate(username=email, password=password)

            if not user:
                raise serializers.ValidationError("Invalid email or password")

        return data