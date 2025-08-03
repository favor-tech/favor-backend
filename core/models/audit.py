from .base import BaseModel
from django.db import models
from django.conf import settings

class Audit(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=255,db_index=True)
    table_name = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = "audit"