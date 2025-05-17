from django.urls import path
from core import views

urlpatterns = [
    path('gallery',views.GalleryView.as_view()),
    path('events/',views.EventsView.as_view()),
    path('eventdetail/',views.EventDetailView.as_view()),
    path('bookmark',views.BookmarkView.as_view()),
]