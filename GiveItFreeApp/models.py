from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class TrustedInstitution(models.Model):
    name = models.CharField(max_length=64)
    purpose = models.CharField(max_length=128)
    localization = models.CharField(max_length=64)
    target_groups = ArrayField(models.CharField(max_length=32))


class Gift(models.Model):
    gift_type = ArrayField(models.CharField(max_length=32))
    number_of_bags = models.SmallIntegerField()
    giver = models.ForeignKey(User, on_delete=models.CASCADE)
    trusted_institution = models.ForeignKey(TrustedInstitution, on_delete=models.CASCADE)
    creation_date = models.DateField(auto_now_add=True)
    transfer_date = models.DateField(null=True)
    is_transferred = models.BooleanField(default=False)
    pick_up_address = models.OneToOneField("PickUpAddress", on_delete=models.CASCADE)


class PickUpAddress(models.Model):
    street = models.CharField(max_length=64)
    city = models.CharField(max_length=32)
    postal_code = models.CharField(max_length=8)
    phone_number = models.CharField(max_length=16)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    comments = models.TextField(null=True)
