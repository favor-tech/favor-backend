from .base import BaseModel
from django.db import models
from rest_framework import serializers

class Location(BaseModel):
    latitude = models.FloatField(db_index=True)
    longitude = models.FloatField(db_index=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    province = models.CharField(max_length=255, null=True, blank=True)
    district = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    timezone = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        obj_name = str(self.province) + ((" / " + str(self.district)) if self.district else "")
        return obj_name


    class Meta:
        db_table = "location"



class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Location
        fields=["id","city","province","district","latitude","longitude"]

