from django.db import models
from .base import BaseModel
from .definitions.DateTimeWithoutTZ import DateTimeWithoutTZField as DateTimeField
from django.conf import settings

class UserRole(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="roles", db_index=True)
    role = models.ForeignKey("Role", on_delete=models.CASCADE, db_index=True,related_name="users")
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assigned_roles", db_index=True)
    assigned_at = DateTimeField(auto_now=True,editable=False)

    class Meta:
        db_table = "user_role"
        unique_together = ("user", "role")

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"
