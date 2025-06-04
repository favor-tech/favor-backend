import os
from .soft_delete import SoftDeleteModel
from django.db import models
from .definitions.DateTimeWithoutTZ import DateTimeWithoutTZField as DateTimeField
from rest_framework import serializers
from django.utils.text import slugify
from core.models.gallery_location import GalleryLocation
def gallery_profile_photo_upload_path(instance, filename):
    gallery_name = slugify(instance.name)
    ext = filename.split('.')[-1]
    filename = f"profile.{ext}"
    return os.path.join("gallery", gallery_name, "profile", filename)

def gallery_cover_photo_upload_path(instance, filename):
    gallery_name = slugify(instance.name)
    ext = filename.split('.')[-1]
    filename = f"cover.{ext}"
    return os.path.join("gallery", gallery_name, "cover", filename)

class Gallery(SoftDeleteModel):
    name = models.CharField(max_length=255,db_index=True,unique=True)
    about = models.TextField()
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=True)
    fax = models.CharField(max_length=50, null=True, blank=True)
    profile_photo = models.ImageField(null=True,blank=True,upload_to=gallery_profile_photo_upload_path)
    cover_photo = models.ImageField(null=True,blank=True,upload_to=gallery_cover_photo_upload_path)
    facebook_url = models.URLField(max_length=500,null=True, blank=True)
    instagram_url = models.URLField(max_length=500,null=True, blank=True)
    linkedin_url = models.URLField(max_length=500,null=True, blank=True)
    tiktok_url = models.URLField(max_length=500,null=True, blank=True)
    web_url = models.URLField(max_length=500,null=True, blank=True)
    x_url = models.URLField(max_length=500,null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "gallery"

class GallerySerializer(serializers.ModelSerializer):
    profile_photo = serializers.ImageField(use_url=True, allow_null=True)
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()

    class Meta:
        model = Gallery
        fields = [
            "id", "name", "about", "profile_photo",
            "latitude", "longitude", "address"
        ]

    def get_latitude(self, obj):
        location = GalleryLocation.objects.filter(gallery=obj).first()
        return location.latitude if location else None

    def get_longitude(self, obj):
        location = GalleryLocation.objects.filter(gallery=obj).first()
        return location.longitude if location else None

    def get_address(self, obj):
        location = GalleryLocation.objects.filter(gallery=obj).first()
        return location.address if location else None
