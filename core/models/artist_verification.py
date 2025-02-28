from .base import BaseModel
from django.db import models
from .definitions.DateTimeWithoutTZ import DateTimeWithoutTZField as DateTimeField

class ArtistVerification(BaseModel):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    artist = models.ForeignKey("Artist", on_delete=models.CASCADE)
    status = models.ForeignKey("UserStatus", on_delete=models.CASCADE)
    approved_by = models.ForeignKey("User", on_delete=models.CASCADE, null=True, blank=True, related_name="approved_verifications")
    rejection_reason = models.TextField(null=True, blank=True)
    requested_at = DateTimeField()
    approved_at = DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "artist_verification"