from django.db import models
from .base import BaseModel

class RolePermission(BaseModel):
    role = models.ForeignKey("Role", on_delete=models.CASCADE, db_index=True)
    permission = models.ForeignKey("Permission", on_delete=models.CASCADE, db_index=True)

    class Meta:
        db_table = "role_permission"
        unique_together = ("role", "permission")

    def __str__(self):
        return f"{self.role.name} - {self.permission.name}"
