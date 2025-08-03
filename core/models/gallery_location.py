import os
from .soft_delete import SoftDeleteModel
from django.db import models
from .definitions.DateTimeWithoutTZ import DateTimeWithoutTZField as DateTimeField
from rest_framework import serializers


class GalleryLocation(SoftDeleteModel):
    gallery = models.ForeignKey("Gallery",on_delete=models.CASCADE,null=True,blank=True,related_name="location")
    latitude = models.FloatField(null=True,blank=True)
    longitude = models.FloatField(null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    province = models.CharField(max_length=255, null=True, blank=True)
    district = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=20, null=True, blank=True)


    class Meta:
        db_table = "gallery_location"

    def __str__(self):
        return str(self.latitude) + " - " + str(self.longitude)

