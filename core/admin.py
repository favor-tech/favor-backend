from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("username", "email", "name", "surname", "is_staff", "is_active")
    search_fields = ("username", "email", "name", "surname")
    ordering = ("username",)

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal Info", {"fields": ("name", "surname", "about", "phone", "profile_picture_url", "instagram_url", "web_url", "x_url")}),
        ("Roles & Permissions", {"fields": ("is_staff", "is_active", "is_superuser")}),
        ("Important dates", {"fields": ("last_login",)}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(RolePermission)
admin.site.register(Event)
admin.site.register(Gallery)
admin.site.register(Artist)
admin.site.register(Location)
admin.site.register(UserLocation)
admin.site.register(UserRole)
