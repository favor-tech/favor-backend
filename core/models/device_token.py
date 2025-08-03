from .base import BaseModel
from django.db import models
from django.conf import settings

class DeviceToken(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    device_token = models.CharField(max_length=255, unique=True)
    platform = models.CharField(max_length=20)
    last_seen = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "device_token"
