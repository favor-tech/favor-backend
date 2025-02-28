from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid
from django.db import models
from django.utils import timezone
from .definitions.DateTimeWithoutTZ import DateTimeWithoutTZField as DateTimeField
from .user_role import UserRole
from .role_permission import RolePermission

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(unique=True, db_index=True)
    surname = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    about = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    artist = models.ForeignKey("Artist", on_delete=models.SET_NULL, null=True, blank=True,related_name="users")
    status = models.ForeignKey("UserStatus", on_delete=models.SET_NULL, null=True, blank=True)
    profile_picture_url = models.URLField(null=True, blank=True)
    instagram_url = models.URLField(null=True, blank=True)
    web_url = models.URLField(null=True, blank=True)
    x_url = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = DateTimeField(editable=False, default=timezone.now)
    updated_at = DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = DateTimeField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "name", "surname"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def get_roles(self):
        return UserRole.objects.filter(user=self).values_list("role__name", flat=True)

    def get_permissions(self):
        roles = UserRole.objects.filter(user=self).values_list("role", flat=True)
        permissions = RolePermission.objects.filter(role__in=roles).values_list("permission__name", flat=True)
        return set(permissions)

    def has_permission(self, permission_name):
        return permission_name in self.get_permissions()
