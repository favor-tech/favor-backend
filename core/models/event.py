from .soft_delete import SoftDeleteModel
from django.db import models
from .definitions.DateTimeWithoutTZ import DateTimeWithoutTZField as DateTimeField

class Event(SoftDeleteModel):
    title = models.CharField(max_length=255,db_index=True)
    gallery = models.ForeignKey("Gallery",on_delete=models.CASCADE)
    location = models.ForeignKey("Location",on_delete=models.CASCADE)
    start_date = DateTimeField(db_index=True)
    end_date = DateTimeField(db_index=True)
    summary = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    buy_ticket_url = models.URLField(null=True, blank=True)
    photos_url = models.URLField(null=True, blank=True)
    thumbnail_url = models.URLField(null=True, blank=True)
    web_url = models.URLField(null=True, blank=True)
    is_free = models.BooleanField()
    price = models.FloatField()
    is_active = models.BooleanField()

    class Meta:
        db_table = "event"