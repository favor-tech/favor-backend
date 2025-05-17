from .base import BaseModel
from django.db import models
from .definitions.DateTimeWithoutTZ import DateTimeWithoutTZField as DateTimeField
from django.conf import settings

class FollowingArtist(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    artist = models.ForeignKey("Artist",on_delete=models.CASCADE)
    followed_at = DateTimeField()
    
    class Meta:
        db_table = "following_artist"