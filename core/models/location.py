from .base import BaseModel
from django.db import models

class Location(BaseModel):
    latitude = models.FloatField(db_index=True)
    longitude = models.FloatField(db_index=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    province = models.CharField(max_length=255, null=True, blank=True)
    district = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    timezone = models.CharField(max_length=255, null=True, blank=True)


    class Meta:
        db_table = "location"