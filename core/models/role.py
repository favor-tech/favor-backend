from django.db import models
from .base import BaseModel

class Role(BaseModel):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    type = models.CharField(max_length=255)
    describe = models.TextField()

    class Meta:
        db_table = "role"

    def __str__(self):
        return self.name
