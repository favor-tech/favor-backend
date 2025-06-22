from .base_views import GenericAPIView, Response
from core.models import Event, Gallery
from core.models.event import EventSerializer
from core.utils.mixins import ApiResponseMixin
from django.utils.timezone import now
from rest_framework import status
from django.http import JsonResponse
from .auth import IsGuestTokenOrAuthenticated

class GalleryEventsView(GenericAPIView, ApiResponseMixin):
    permission_classes = [IsGuestTokenOrAuthenticated]

    def get(self, request):
        gallery_id = request.GET.get("gallery")

        if not gallery_id:
            return JsonResponse({"error": "Gallery ID is required."}, status=400)

        try:
            gallery = Gallery.objects.get(id=gallery_id)
            current_time = now()

            all_events = Event.objects.filter(gallery=gallery, is_active=True)

            past_events = all_events.filter(end_date__lt=current_time).order_by("-start_date")
            ongoing_events = all_events.filter(start_date__lte=current_time, end_date__gte=current_time).order_by("start_date")
            upcoming_events = all_events.filter(start_date__gt=current_time).order_by("start_date")

            context = {"request": request}
            data = {
                "past_events": EventSerializer(past_events, many=True, context=context).data,
                "ongoing_events": EventSerializer(ongoing_events, many=True, context=context).data,
                "upcoming_events": EventSerializer(upcoming_events, many=True, context=context).data,
            }

            return self.api_response(success=True, message="Success", data=data, status_code=status.HTTP_200_OK)

        except Gallery.DoesNotExist:
            return JsonResponse({"error": "Gallery not found."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
