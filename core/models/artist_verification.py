from .base import BaseModel
from django.db import models
from .definitions.DateTimeWithoutTZ import DateTimeWithoutTZField as DateTimeField
from django.conf import settings

class ArtistVerification(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    artist = models.ForeignKey("Artist", on_delete=models.CASCADE)
    status = models.ForeignKey("UserStatus", on_delete=models.SET_NULL, null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_verifications")
    rejection_reason = models.TextField(null=True, blank=True)
    requested_at = DateTimeField(editable=False)
    approved_at = DateTimeField(auto_now=True,editable=False)

    class Meta:
        db_table = "artist_verification"