from .base import BaseModel
from django.db import models
from .definitions.DateTimeWithoutTZ import DateTimeWithoutTZField as DateTimeField
from django.conf import settings
from rest_framework import serializers
from core.models.event import Event
from core.models.user import User
class Bookmark(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="app_bookmark")
    event = models.ForeignKey("Event",on_delete=models.CASCADE)
    bookmarked_at = DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "bookmark"


class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","email","name","surname"]

class EventMiniSerializer(serializers.ModelSerializer):
    gallery_name = serializers.CharField(source="gallery.name", read_only=True)
    gallery_location_address = serializers.CharField(source="gallery_location.address", read_only=True)
    
    class Meta:
        model = Event
        fields = ["id", "title", "start_date", "end_date","gallery","gallery_name","gallery_location_address"] 

class BookmarkSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(read_only=True)
    event = EventMiniSerializer(read_only=True)
    
    class Meta:
        model=Bookmark
        fields=["user","event","bookmarked_at"]
