from .base import BaseModel
from django.db import models

class GeneralNotification(BaseModel):
    title = models.CharField(max_length=255)
    message = models.TextField()
    redirect_url = models.URLField(null=True, blank=True)
    is_sent = models.BooleanField(default=False)

    class Meta:
        db_table = "general_notification"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
