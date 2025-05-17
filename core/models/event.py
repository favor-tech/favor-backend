import os
from .soft_delete import SoftDeleteModel
from django.db import models
from .definitions.DateTimeWithoutTZ import DateTimeWithoutTZField as DateTimeField
from rest_framework import serializers
from django.utils.text import slugify




def event_thumbnail_upload_path(instance, filename):
    title = slugify(instance.title)
    ext = filename.split('.')[-1]
    filename = f"thumbnail.{ext}"
    return os.path.join("events", title, "thumbnail", filename)

class Event(SoftDeleteModel):
    title = models.CharField(max_length=255,db_index=True)
    gallery = models.ForeignKey("Gallery",on_delete=models.CASCADE,blank=True,null=True)
    location = models.ForeignKey("Location",on_delete=models.CASCADE,blank=True,null=True)
    start_date = DateTimeField(db_index=True)
    end_date = DateTimeField(db_index=True)
    summary = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    buy_ticket_url = models.URLField(max_length=500,null=True, blank=True)
    thumbnail_image = models.ImageField(null=True,blank=True,upload_to=event_thumbnail_upload_path)   
    web_url = models.URLField(max_length=500,null=True, blank=True)
    is_free = models.BooleanField(default=False)
    price = models.FloatField(null=True,blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "event"


class EventSerializer(serializers.ModelSerializer):
    thumbnail_image = serializers.ImageField(use_url=True, allow_null=True)

    class Meta:
        model=Event
        fields=["id","title","start_date","end_date","gallery","web_url","description","thumbnail_image","buy_ticket_url","is_free","price","is_active"]
