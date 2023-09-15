from rest_framework import serializers
from .models import PhoneNumber, CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "password",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
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


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = "__all__"


class ImageUploadSerializer(serializers.Serializer):
    image_file = serializers.FileField()


class WhatsAppBulkMessageSerializer(serializers.Serializer):
    numbers = serializers.ListField(child=serializers.CharField(max_length=20))
    template_name = serializers.CharField()


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
