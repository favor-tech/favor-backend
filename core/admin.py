from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.contrib import admin
from django import forms
from .forms import EventForm
from core.services.firebase_service import send_push_to_user
from django.contrib import messages

admin.site.site_header = "Favor Admin Panel"
admin.site.site_title = "Favor Administration"
admin.site.index_title = "Welcome to Favor Admin"

class ArtistModelAdmin(admin.ModelAdmin):
    search_fields = ["name","surname"]
    list_display = ["name","surname"]



class EventArtistInline(admin.TabularInline):
    model = EventArtist
    extra = 1
    autocomplete_fields = ['artist']
class EventCategoryInline(admin.TabularInline):
    model = EventCategory
    extra = 1
    autocomplete_fields = ['category']

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name']
    ordering = ['name']

class EventImagesInline(admin.TabularInline):
    model = EventImages
    extra = 1

class EventModelAdmin(admin.ModelAdmin):
    form = EventForm
    inlines = [EventArtistInline,EventCategoryInline,EventImagesInline]
    autocomplete_fields = ['gallery']
    search_fields = ["title","start_date","end_date"]
    list_display = ["title","gallery","gallery_location","start_date","end_date","is_indefinite"]



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
    ordering = ['name']


class GalleryLocationAdmin(admin.ModelAdmin):
    model = GalleryLocation
    search_fields = ["latitude","longitude","address","gallery__name"]
    list_display = ["get_gallery_name","latitude","longitude","province","district","address"]
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
    list_display = ("username", "email", "name", "surname", "is_staff", "is_active","providers")
    search_fields = ("username", "email", "name", "surname")
    ordering = ("username",)

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal Info", {"fields": ("name", "surname","birthdate" ,"about", "artist","phone", "profile_picture", "instagram_url", "web_url", "x_url","facebook_url","linkedin_url")}),
        ("Roles & Permissions", {"fields": ("is_staff", "is_active", "is_superuser")}),
        #("Important dates", {"fields": ("last_login",)}),
    )

models = [Role,Permission,RolePermission,GalleryArtist,GalleryUser,UserLocation,UserRole,UserStatus,
          ArtistVerification,ArtistStatus]


class BookmarkAdmin(admin.ModelAdmin):
    search_fields = ["bookmarked_at"]
    list_display = ["user","event","bookmarked_at"]

class GeneralNotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "message", "created_at")
    actions = ["send_push_to_all"]

    def send_push_to_all(self, request, queryset):
        for notification in queryset:
            users = User.objects.all()
            for user in users:
                send_push_to_user(
                    user,
                    notification.title,
                    notification.message,
                    redirect_url=None
                )
        self.message_user(request, f"{queryset.count()} bildirim gönderildi.", messages.SUCCESS)

    send_push_to_all.short_description = "Seçili bildirimleri tüm kullanıcılara gönder"

class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "message", "is_read", "sent_at")
    actions = ["send_push_to_user"]

    def send_push_to_user(self, request, queryset):
        for notification in queryset:
            send_push_to_user(
                notification.user,
                notification.title,
                notification.message,
                notification.redirect_url
            )
        self.message_user(request, f"{queryset.count()} bildirim kullanıcıya gönderildi.", messages.SUCCESS)

    send_push_to_user.short_description = "Seçili bildirimleri ilgili kullanıcıya gönder"



for model in models:
    admin.site.register(model)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Artist,ArtistModelAdmin)
admin.site.register(Event, EventModelAdmin)
admin.site.register(GalleryLocation,GalleryLocationAdmin)
admin.site.register(Location,LocationAdmin)
admin.site.register(Gallery,GalleryAdmin)
admin.site.register(Bookmark,BookmarkAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(GeneralNotification, GeneralNotificationAdmin)
admin.site.register(Notification, NotificationAdmin)