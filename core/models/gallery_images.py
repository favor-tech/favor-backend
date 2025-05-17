from .base import BaseModel
from django.db import models
import os
from django.utils.text import slugify


def gallery_image_upload_path(instance, filename):
    name = slugify(instance.gallery.name)
    return os.path.join("gallery", name, "images", filename)


class GalleryImages(BaseModel):
    gallery = models.ForeignKey("Gallery",on_delete=models.CASCADE,related_name="gallery_images")
    image = models.ImageField(upload_to=gallery_image_upload_path)

    class Meta:
        db_table = "gallery_images"