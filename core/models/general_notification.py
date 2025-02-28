from .base import BaseModel
from django.db import models

class GeneralNotification(BaseModel):
    title = models.CharField(max_length=255)
    message = models.TextField()

    class Meta:
        db_table = "general_notification"