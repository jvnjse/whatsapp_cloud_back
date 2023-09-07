from rest_framework import serializers
from .models import PhoneNumber


class ExcelSerializer(serializers.Serializer):
    excel_file = serializers.FileField()


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = "__all__"


class WhatsAppBulkMessageSerializer(serializers.Serializer):
    numbers = serializers.ListField(child=serializers.CharField(max_length=20))
