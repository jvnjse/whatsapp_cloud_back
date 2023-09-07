from rest_framework import serializers


class PhoneNumberSerializer(serializers.Serializer):
    excel_file = serializers.FileField()
