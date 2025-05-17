from .base import BaseModel
from django.db import models

class ExhibitionTypes(BaseModel):
    name = models.CharField(unique=True,max_length=255,db_index=True)
    keywords = models.JSONField(null=True,blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "exhibition_types"