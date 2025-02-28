from .base import BaseModel
from django.db import models

class GalleryUser(BaseModel):
    gallery = models.ForeignKey("Gallery", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    role = models.ForeignKey("Role", on_delete=models.CASCADE)

    class Meta:
        db_table ="gallery_user"