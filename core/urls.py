from django.urls import path
from core import views

urlpatterns = [
    path('gallery',views.GalleryView.as_view()),
    path('events/',views.EventsView.as_view()),
    path('eventdetail/',views.EventDetailView.as_view()),
    path('bookmark',views.BookmarkView.as_view()),
    path('artistprofile',views.ArtistProfileView.as_view()),
    path('userprofile',views.UserProfileView.as_view()),
    path('bookmarklist',views.BookmarkListView.as_view()),
    path('galleryprofile',views.GalleryProfileView.as_view()),
    path('accountsettings',views.AccountSettingsView.as_view()),
    path('artistevents',views.ArtistEventsView.as_view()),
    path('galleryevents',views.GalleryEventsView.as_view())
]