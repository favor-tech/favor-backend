from .base import BaseModel
from django.db import models
from .definitions.DateTimeWithoutTZ import DateTimeWithoutTZField as DateTimeField

class Blacklist(BaseModel):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    banned_by = models.ForeignKey("User", on_delete=models.CASCADE, related_name="banned_users")
    reason = models.TextField()
    ban_type = models.CharField(max_length=10, choices=[("TEMP", "Temporary"), ("PER", "Permanent")])
    banned_until = DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "blacklist"