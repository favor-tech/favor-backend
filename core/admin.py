from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.contrib import admin
from django import forms


class EventModelAdminForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class EventModelAdmin(admin.ModelAdmin):
    form = EventModelAdminForm


class LocationAdmin(admin.ModelAdmin):
    search_fields = ["city", "province", "district", "region","latitude","longitude", "country", "timezone"]
    list_display = ["city", "province", "district", "region", "latitude","longitude", "country", "timezone"]

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("username", "email", "name", "surname", "is_staff", "is_active")
    search_fields = ("username", "email", "name", "surname")
    ordering = ("username",)

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal Info", {"fields": ("name", "surname", "about", "artist","phone", "profile_picture_url", "instagram_url", "web_url", "x_url")}),
        ("Roles & Permissions", {"fields": ("is_staff", "is_active", "is_superuser")}),
        #("Important dates", {"fields": ("last_login",)}),
    )

models = [Role,Permission,RolePermission,Gallery,GalleryArtist,GalleryUser,EventArtist,
          EventCategory,Artist,Category,UserLocation,UserRole,UserStatus,
          ArtistVerification,ArtistStatus]

for model in models:
    admin.site.register(model)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Event, EventModelAdmin)
admin.site.register(Location,LocationAdmin)