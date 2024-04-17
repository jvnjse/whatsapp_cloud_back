from rest_framework import serializers
from .models import PhoneNumber, CustomUser, Template, ContactForm, PlanPurchase
import random
import string
from .functions.tasks import send_email

# from django.core.mail import send_mail, EmailMultiAlternatives
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags
# from django.conf import settings
import datetime
import pandas as pd


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
            "first_name",
            "last_name",
            "phone",
            "company_name",
            "trial_plan",
            "referral_string",
            "register_date",
            "basic_feature",
            "standard_feature",
            "advanced_feature",
        )
        # extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        email = validated_data.get("email")
        first_name = validated_data.get("first_name")
        last_name = validated_data.get("last_name")
        is_active = validated_data.get("is_active", True)
        is_staff = validated_data.get("is_staff", False)
        trial_user = validated_data.get("trial_user", True)
        is_distributor = validated_data.get("is_distributor", False)
        phone = validated_data.get("phone")
        company_name = validated_data.get("company_name")
        trial_plan = validated_data.get("trial_plan")
        referral_string = validated_data.get("referral_string")
        basic_feature = False
        standard_feature = False
        advanced_feature = False

        if trial_plan == "basic":
            basic_feature = True
        elif trial_plan == "standard":
            standard_feature = True
        elif trial_plan == "advanced":
            advanced_feature = True

        password = "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(6)
        )

        instance = self.Meta.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_active=is_active,
            is_staff=is_staff,
            is_distributor=is_distributor,
            phone=phone,
            company_name=company_name,
            trial_plan=trial_plan,
            trial_user=trial_user,
            basic_feature=basic_feature,
            standard_feature=standard_feature,
            advanced_feature=advanced_feature,
        )
        instance.set_password(password)

        if referral_string:
            try:
                parent_user = CustomUser.objects.get(referral_string=referral_string)
                instance.parent_user = parent_user
                instance.save()
            except CustomUser.DoesNotExist:
                pass

        send_email.delay(email, password)
        instance.register_date = datetime.date.today()
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
            "trial_user",
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
    app_id = serializers.CharField()


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


class PlanPurchaseSerializer(serializers.ModelSerializer):
    user_first_name = serializers.SerializerMethodField()
    user_last_name = serializers.SerializerMethodField()

    def get_user_first_name(self, obj):
        return obj.user.first_name

    def get_user_last_name(self, obj):
        return obj.user.last_name

    class Meta:
        model = PlanPurchase
        fields = [
            "id",
            "user",
            "user_first_name",
            "user_last_name",
            "plan",
            "started_date",
            "image",
        ]
