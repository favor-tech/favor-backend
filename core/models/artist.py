from .base import BaseModel
from django.db import models
from .definitions.DateTimeWithoutTZ import DateTimeWithoutTZField as DateTimeField

class Artist(BaseModel):
    name = models.CharField(max_length=255,db_index=True)
    surname = models.CharField(max_length=255,db_index=True)
    about = models.TextField()
    user = models.ForeignKey("User",on_delete=models.CASCADE,related_name="artist_profile")
    is_registered = models.BooleanField()
    registered_at = DateTimeField(null=True, blank=True,auto_now=True,editable=False)
    x_url = models.URLField(null=True, blank=True)
    instagram_url = models.URLField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    profile_picture_url = models.URLField(null=True, blank=True)
    web_url = models.URLField(null=True, blank=True)

    class Meta:
        db_table = "artist"