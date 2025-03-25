from .soft_delete import SoftDeleteModel
from django.db import models
from .definitions.DateTimeWithoutTZ import DateTimeWithoutTZField as DateTimeField

class Event(SoftDeleteModel):
    title = models.CharField(max_length=255,db_index=True)
    gallery = models.ForeignKey("Gallery",on_delete=models.CASCADE,blank=True,null=True)
    location = models.ForeignKey("Location",on_delete=models.CASCADE,blank=True,null=True)
    start_date = DateTimeField(db_index=True)
    end_date = DateTimeField(db_index=True)
    summary = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    buy_ticket_url = models.URLField(max_length=500,null=True, blank=True)
    photos_url = models.URLField(max_length=500,null=True, blank=True)
    thumbnail_url = models.URLField(max_length=500,null=True, blank=True)
    web_url = models.URLField(max_length=500,null=True, blank=True)
    is_free = models.BooleanField(default=False)
    price = models.FloatField(null=True,blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "event"