from rest_framework import serializers
from GiveItFreeApp.models import PickUpAddress, Gift


class TrustedInstitutionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=64)
    purpose = serializers.CharField(max_length=128)


class PickUpAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickUpAddress
        fields = ('street', 'city', 'postal_code', 'phone_number', 'pick_up_date', 'pick_up_time', 'comments')


class GiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gift
        fields = ('gift_type', 'number_of_bags', 'trusted_institution')
