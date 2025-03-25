from .soft_delete import SoftDeleteModel
from django.db import models
from .definitions.DateTimeWithoutTZ import DateTimeWithoutTZField as DateTimeField

class Gallery(SoftDeleteModel):
    name = models.CharField(max_length=255,db_index=True,unique=True)
    about = models.TextField()
    address = models.TextField(blank=True,null=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    location = models.ForeignKey("Location",on_delete=models.CASCADE,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=True)
    fax = models.CharField(max_length=50, null=True, blank=True)
    cover_photo_url = models.URLField(max_length=500,null=True,blank=True)
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