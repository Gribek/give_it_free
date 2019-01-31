from rest_framework import serializers


class TrustedInstitutionSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=64)
    purpose = serializers.CharField(max_length=128)
