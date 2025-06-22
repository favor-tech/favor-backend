from .base_views import GenericAPIView, Response, IsAuthenticated
from core.models import EventArtist, Event, Artist
from core.utils.mixins import ApiResponseMixin
from django.http import JsonResponse
from rest_framework import status
from django.utils.timezone import now
from .auth import IsGuestTokenOrAuthenticated
from core.models.event import Event, EventSerializer

class ArtistEventsView(GenericAPIView, ApiResponseMixin):
    permission_classes = [IsGuestTokenOrAuthenticated]

    def get(self, request):
        artist_id = request.GET.get("artist")

        if not artist_id:
            return JsonResponse({"error": "Artist ID is required."}, status=400)

        try:
            artist = Artist.objects.get(id=artist_id)

            event_ids = EventArtist.objects.filter(artist=artist).values_list("event_id", flat=True)

            events = Event.objects.filter(id__in=event_ids, start_date__lte=now()).order_by("-start_date")

            serialized = EventSerializer(events, many=True, context={"request": request})

            return self.api_response(success=True, message="Success", data=serialized.data, status_code=status.HTTP_200_OK)

        except Artist.DoesNotExist:
            return JsonResponse({"error": "Artist not found."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
