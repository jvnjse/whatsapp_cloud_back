from rest_framework import serializers
from .models import PhoneNumber, CustomUser
import random
import string
from django.core.mail import send_mail


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
        )
        # extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        email = validated_data.get("email")

        # Generate a random password
        password = "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(6)
        )

        # Create the user instance with the email and set the password
        instance = self.Meta.model(email=email)
        instance.set_password(password)
        instance.save()

        # Send the random password to the provided email address
        send_mail(
            subject="Your New Account Password",
            message=f"Your password is: {password}",
            from_email="jeevanjose2016@gmail.com",  # Change this to your email address
            recipient_list=[email],
            fail_silently=False,  # Set to True to suppress errors if email fails to send
        )

        return instance


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid email")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid password")

        attrs["user"] = user
        return attrs


class ExcelSerializer(serializers.Serializer):
    excel_file = serializers.FileField()
    template_name = serializers.CharField(required=False)


class ExcelImageSerializer(serializers.Serializer):
    excel_file = serializers.FileField()
    template_name = serializers.CharField(required=False)
    image_link = serializers.CharField()


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = "__all__"


class ImageUploadSerializer(serializers.Serializer):
    image_file = serializers.FileField()


class WhatsAppBulkMessageSerializer(serializers.Serializer):
    numbers = serializers.ListField(child=serializers.CharField(max_length=20))
    template_name = serializers.CharField()


class WhatsAppBulkMessageImageSerializer(serializers.Serializer):
    numbers = serializers.ListField(child=serializers.CharField(max_length=20))
    template_name = serializers.CharField()
    image_link = serializers.CharField()


class MessageTemplateSerializer(serializers.Serializer):
    template_name = serializers.CharField(required=False)
    header_text = serializers.CharField(required=False)
    body_text = serializers.CharField(required=False)
    footer_text = serializers.CharField(required=False)
    button_type = serializers.CharField(required=False)
    button_text = serializers.CharField(required=False)
    button_url = serializers.CharField(required=False)
    category = serializers.CharField(required=False)
    language = serializers.CharField(required=False)


class MessageTextTemplateSerializer(serializers.Serializer):
    template_name = serializers.CharField(required=False)
    header_text = serializers.CharField(required=False)
    body_text = serializers.CharField(required=False)
    footer_text = serializers.CharField(required=False)
