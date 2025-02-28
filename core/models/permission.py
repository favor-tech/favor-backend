from .base import BaseModel
from django.db import models

class Permission(BaseModel):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    type = models.CharField(max_length=255,db_index=True)
    describe = models.TextField()

    class Meta:
        db_table = "permission"

    def __str__(self):
        return self.name
