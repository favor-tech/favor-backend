from django.db import models
from .base import BaseModel

class EventTypes(BaseModel):
    event = models.ForeignKey("Event",on_delete=models.CASCADE)
    exhibition_type = models.ForeignKey("ExhibitionTypes",on_delete=models.CASCADE)

    def __str__(self):
        return self.event.title + " - " + self.exhibition_type.name

    class Meta:
        db_table = "event_types"