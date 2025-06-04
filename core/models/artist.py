import os
from .base import BaseModel
from django.db import models
from .definitions.DateTimeWithoutTZ import DateTimeWithoutTZField as DateTimeField
from django.conf import settings
from django.utils.text import slugify
from rest_framework import serializers


def artist_profile_picture_upload_path(instance, filename):
    artist_name = slugify(instance.name)
    artist_surname = slugify(instance.surname)
    ext = filename.split('.')[-1]
    filename = f"profile.{ext}"
    return os.path.join("artists",f"{artist_name}_{artist_surname}","profilepictures",filename)

class Artist(BaseModel):
    name = models.CharField(max_length=255, db_index=True)
    surname = models.CharField(max_length=255, db_index=True)
    about = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="artist_profile")
    email = models.EmailField(unique=True, db_index=True, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    is_registered = models.BooleanField()
    registered_at = DateTimeField(null=True, blank=True, auto_now=True, editable=False)
    x_url = models.URLField(max_length=500, null=True, blank=True)
    instagram_url = models.URLField(max_length=500, null=True, blank=True)
    linkedin_url = models.URLField(max_length=500, null=True, blank=True)
    profile_picture = models.ImageField(upload_to=artist_profile_picture_upload_path,null=True,blank=True)
    web_url = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.surname}"

    class Meta:
        db_table = "artist"


class ArtistSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(use_url=True, allow_null=True)

    class Meta:
        model = Artist
        fields = ["id", "name", "surname", "about", "profile_picture"]
