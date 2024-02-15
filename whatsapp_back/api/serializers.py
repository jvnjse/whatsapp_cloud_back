from rest_framework import serializers
from .models import PhoneNumber, CustomUser, Template, ContactForm
import random
import string
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


class CustomUserSerializer(serializers.ModelSerializer):
    referral_string = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "is_active",
            "is_staff",
            "is_distributor",
            "referral_string",
        )
        # extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        email = validated_data.get("email")
        referral_string = validated_data.get("referral_string")

        password = "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(6)
        )

        instance = self.Meta.model(email=email)
        instance.set_password(password)

        if referral_string:
            try:
                parent_user = CustomUser.objects.get(referral_string=referral_string)
                instance.parent_user = parent_user
                instance.save()
            except CustomUser.DoesNotExist:
                pass
        my_subject = "Whatsapp Module Generated Password"
        context = {
            "password": password,
        }
        recipient_list = [email]
        html_message = render_to_string("password.html", context)
        plain_message = strip_tags(html_message)
        message = EmailMultiAlternatives(
            subject=my_subject,
            body=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=recipient_list,
        )
        message.attach_alternative(html_message, "text/html")
        message.send()
        # send_mail(
        #     subject="Your New Account Password",
        #     message=f"Your password is: {password}",
        #     from_email="jeevanjose2016@gmail.com",
        #     recipient_list=[email],
        #     fail_silently=False,
        # )
        instance.save()
        return instance


class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            # "id",
            "email",
            "is_active",
            "is_staff",
            "is_distributor",
            "basic_feature",
            "standard_feature",
            "advanced_feature",
        )


class ReferalStringSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "referral_string"]


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
    user_id = serializers.IntegerField()


class ExcelImageSerializer(serializers.Serializer):
    excel_file = serializers.FileField()
    template_name = serializers.CharField(required=False)
    user_id = serializers.IntegerField()
    image_link = serializers.CharField()


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = "__all__"


class ImageUploadSerializer(serializers.ModelSerializer):
    # template_name = serializers.CharField(max_length=30)
    # template_image = serializers.ImageField(use_url=False)

    class Meta:
        model = Template
        fields = ["template_name", "template_image"]


class CredentialsSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    phone_number_id = serializers.CharField()
    whatsapp_business_id = serializers.CharField()
    permanent_access_token = serializers.CharField()


class WhatsAppBulkMessageSerializer(serializers.Serializer):
    numbers = serializers.ListField(child=serializers.CharField(max_length=20))
    user_id = serializers.IntegerField()
    template_name = serializers.CharField()


class WhatsAppBulkMessageImageSerializer(serializers.Serializer):
    numbers = serializers.ListField(child=serializers.CharField(max_length=20))
    template_name = serializers.CharField()
    image_link = serializers.CharField()
    user_id = serializers.CharField()


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


class ScheduledAPISerializer(serializers.Serializer):
    scheduled_time = serializers.DateTimeField()
    api_data = serializers.CharField()


class ContactFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactForm
        fields = "__all__"
