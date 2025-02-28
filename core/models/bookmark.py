from .base import BaseModel
from django.db import models
from .definitions.DateTimeWithoutTZ import DateTimeWithoutTZField as DateTimeField

class Bookmark(BaseModel):
    user = models.ForeignKey("User",on_delete=models.CASCADE,related_name="app_bookmark")
    event = models.ForeignKey("Event",on_delete=models.CASCADE)
    bookmarked_at = DateTimeField()

    class Meta:
        db_table = "bookmark"