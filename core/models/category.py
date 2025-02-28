from .base import BaseModel
from django.db import models

class Category(BaseModel):
    name = models.CharField(max_length=255,db_index=True)
    keywords = models.JSONField() #??????


    class Meta:
        db_table = "category"