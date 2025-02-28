from .base import BaseModel
from django.db import models
from .definitions.DateTimeWithoutTZ import DateTimeWithoutTZField as DateTimeField

class FollowingArtist(BaseModel):
    user = models.ForeignKey("User",on_delete=models.CASCADE)
    artist = models.ForeignKey("Artist",on_delete=models.CASCADE)
    followed_at = DateTimeField()
    
    class Meta:
        db_table = "following_artist"