from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.contrib import admin
from django import forms
from datetime import datetime , time
from .forms import EventForm


class EventArtistInline(admin.TabularInline):
    model = EventArtist
    extra = 1

class EventCategoryInline(admin.TabularInline):
    model = EventCategory
    extra = 1

class EventImagesInline(admin.TabularInline):
    model = EventImages
    extra = 1

class EventModelAdminForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'  

        # widgets = {
        #    'start_date': forms.DateInput(attrs={'type': 'date'}),
        #    'end_date': forms.DateInput(attrs={'type': 'date'}),
        # }

class EventModelAdmin(admin.ModelAdmin):
    form = EventForm
    inlines = [EventArtistInline,EventCategoryInline,EventImagesInline]

    search_fields = ["title","start_date","end_date"]
    list_display = ["title","gallery","gallery_location","start_date","end_date"]
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
    
        if db_field.name == "gallery_location":
            if request._obj_ is not None:
                kwargs["queryset"] = GalleryLocation.objects.filter(gallery=request._obj_.gallery)
            else:
                kwargs["queryset"] = GalleryLocation.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        request._obj_ = obj
        return super().get_form(request, obj, **kwargs)


class GalleryImagesInline(admin.TabularInline):
    model = GalleryImages
    extra = 1

class GalleryLocationInline(admin.TabularInline):
    model = GalleryLocation
    extra = 1
    fields = ('address','latitude', 'longitude')
    can_delete = False
class GalleryAdmin(admin.ModelAdmin):
    inlines = [GalleryLocationInline,GalleryImagesInline]   
    search_fields = ["name"]
    list_display = ["name"]


class GalleryLocationAdmin(admin.ModelAdmin):
    model = GalleryLocation
    search_fields = ["latitude","longitude","address","gallery__name"]
    list_display = ["get_gallery_name","latitude","longitude","address"]
    def get_gallery_name(self, obj):
            return obj.gallery.name if obj.gallery else "-"
    get_gallery_name.short_description = "Gallery"

class LocationAdmin(admin.ModelAdmin):
    search_fields = ["city", "province", "district", "region","latitude","longitude", "country", "timezone"]
    list_display = ["city", "province", "district", "region", "latitude","longitude", "country", "timezone"]

class UserRoleInline(admin.TabularInline):
    model = UserRole
    extra = 1
    fk_name = "user"

class CustomUserAdmin(UserAdmin):
    model = User
    inlines = [UserRoleInline]
    list_display = ("username", "email", "name", "surname", "is_staff", "is_active")
    search_fields = ("username", "email", "name", "surname")
    ordering = ("username",)

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal Info", {"fields": ("name", "surname","birthdate" ,"about", "artist","phone", "profile_picture", "instagram_url", "web_url", "x_url")}),
        ("Roles & Permissions", {"fields": ("is_staff", "is_active", "is_superuser")}),
        #("Important dates", {"fields": ("last_login",)}),
    )

models = [Role,Permission,RolePermission,GalleryArtist,GalleryUser,Artist,Category,UserLocation,UserRole,UserStatus,
          ArtistVerification,ArtistStatus]


class BookmarkAdmin(admin.ModelAdmin):
    search_fields = ["bookmarked_at"]
    list_display = ["user","event","bookmarked_at"]

for model in models:
    admin.site.register(model)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Event, EventModelAdmin)
admin.site.register(GalleryLocation,GalleryLocationAdmin)
admin.site.register(Location,LocationAdmin)
admin.site.register(Gallery,GalleryAdmin)
admin.site.register(Bookmark,BookmarkAdmin)