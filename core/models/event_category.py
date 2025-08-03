from django.db import models
from .base import BaseModel

class EventCategory(BaseModel):
    event = models.ForeignKey("Event",on_delete=models.CASCADE)
    category = models.ForeignKey("Category",on_delete=models.CASCADE)

    def __str__(self):
        return self.event.title + " - " + self.category.name

    class Meta:
        db_table = "event_category"