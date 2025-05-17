from .base import BaseModel
from django.db import models
from rest_framework import serializers
import os
from django.utils.text import slugify


def event_image_upload_path(instance, filename):
    title = slugify(instance.event.title)
    return os.path.join("events", title, "images", filename)

class EventImages(BaseModel):
    event = models.ForeignKey("Event",on_delete=models.CASCADE,related_name="event_images")
    image = models.ImageField(upload_to=event_image_upload_path)

    class Meta:
        db_table = "event_images"


class EventImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = EventImages
        fields = ['image']