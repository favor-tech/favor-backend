from .base import BaseModel
from django.db import models
from .definitions.DateTimeWithoutTZ import DateTimeWithoutTZField as DateTimeField

class UserLocation(BaseModel):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    location = models.ForeignKey("Location", on_delete=models.CASCADE)
    detected_at = DateTimeField()
    is_active = models.BooleanField()

    class Meta:
        db_table = "user_location"