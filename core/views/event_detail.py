import json
from .base_views import GenericAPIView, Response, IsAuthenticated
from .auth import IsGuestTokenOrAuthenticated
from core.models import *
from django.http import JsonResponse
from core.utils.mixins import ApiResponseMixin
from rest_framework import status


class EventDetailView(GenericAPIView, ApiResponseMixin):
    permission_classes = [IsGuestTokenOrAuthenticated]
    #permission_classes = [IsAuthenticated]

    def get(self, request):
        event_id = request.GET.get('event')

        if not event_id:
            return JsonResponse({'error': 'Event ID is required.'}, status=400)

        try:
            event = Event.objects.get(id=event_id)
            gallery = event.gallery
            event_artists = EventArtist.objects.filter(event=event)
            artists = [ArtistSerializer(ea.artist).data for ea in event_artists]

            event_images = EventImages.objects.filter(event=event)
            image_urls = [img.image.url for img in event_images if img.image]

            serialized = {
                'event': EventSerializer(event).data,
                'gallery': GallerySerializer(gallery).data,
                'artists': artists,
                'images': image_urls,
            }

            return self.api_response(success=True, message="Success", data=serialized, status_code=status.HTTP_200_OK)
        except Event.DoesNotExist:
            return self.api_response(success=False, message="Event not found.", status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return self.api_response(success=False, message=str(e), status_code=status.HTTP_400_BAD_REQUEST)