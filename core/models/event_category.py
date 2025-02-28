from django.db import models
from .base import BaseModel

class EventCategory(BaseModel):
    event = models.ForeignKey("Event",on_delete=models.CASCADE)
    category = models.ForeignKey("Category",on_delete=models.CASCADE)

    class Meta:
        db_table = "event_category"