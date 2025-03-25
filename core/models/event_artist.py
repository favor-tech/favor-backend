from django.db import models
from .base import BaseModel


class EventArtist(BaseModel):
    event = models.ForeignKey("Event",on_delete=models.CASCADE)
    artist = models.ForeignKey("Artist",on_delete=models.CASCADE)

    def __str__(self):
        return self.event.title + " - " + self.artist.name + " " + self.artist.surname

    class Meta:
        db_table = "event_artist"