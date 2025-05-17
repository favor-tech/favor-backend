from .base import BaseModel
from django.db import models
from .definitions.DateTimeWithoutTZ import DateTimeWithoutTZField as DateTimeField
from django.conf import settings

class Bookmark(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="app_bookmark")
    event = models.ForeignKey("Event",on_delete=models.CASCADE)
    bookmarked_at = DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "bookmark"