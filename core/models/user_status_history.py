from .base import BaseModel
from django.db import models
from .definitions.DateTimeWithoutTZ import DateTimeWithoutTZField as DateTimeField

class UserStatusHistory(BaseModel):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    status = models.ForeignKey("UserStatus", on_delete=models.CASCADE)
    changed_by = models.ForeignKey("User", on_delete=models.CASCADE, related_name="changed_statuses")
    reason = models.TextField()
    changed_at = DateTimeField()

    class Meta:
        db_table = "user_status_history"