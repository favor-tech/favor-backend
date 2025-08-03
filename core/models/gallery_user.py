from .base import BaseModel
from django.db import models
from django.conf import settings

class GalleryUser(BaseModel):
    gallery = models.ForeignKey("Gallery", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.ForeignKey("Role", on_delete=models.CASCADE)

    class Meta:
        db_table ="gallery_user"