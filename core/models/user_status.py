from .base import BaseModel
from django.db import models

class UserStatus(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "user_status"