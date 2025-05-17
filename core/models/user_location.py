from .base import BaseModel
from django.db import models
from .definitions.DateTimeWithoutTZ import DateTimeWithoutTZField as DateTimeField
from django.conf import settings

class UserLocation(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location = models.ForeignKey("Location", on_delete=models.CASCADE)
    detected_at = DateTimeField(editable=False)
    is_active = models.BooleanField()

    class Meta:
        db_table = "user_location"