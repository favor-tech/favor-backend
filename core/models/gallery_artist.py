from .base import BaseModel
from django.db import models

class GalleryArtist(BaseModel):
    gallery = models.ForeignKey("Gallery", on_delete=models.CASCADE)
    artist = models.ForeignKey("Artist", on_delete=models.CASCADE)

    class Meta:
        db_table = "gallery_artist"