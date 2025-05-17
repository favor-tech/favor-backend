import json
from .base_views import GenericAPIView, Response, IsAuthenticated
from core.models import *
from django.http import JsonResponse
from core.utils.mixins import ApiResponseMixin
from rest_framework import status
from django.db.models import Count
from django.utils import timezone
from datetime import datetime

class EventsView(GenericAPIView, ApiResponseMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')
        is_free = request.GET.get('is_free')

        if is_free:
            is_free = is_free.lower() == 'true'
        else:
            is_free = None

        if not latitude or not longitude:
            return JsonResponse({'error': 'latitude and longitude are required'}, status=400)

        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            return JsonResponse({'error': 'Invalid latitude or longitude'}, status=400)

        nearby_locations = self.filter_nearby_locations(latitude, longitude)
        events = Event.objects.filter(location__in=nearby_locations)

        if is_free:
            events = events.filter(is_free=is_free)


        start_date = request.GET.get("start")
        end_date = request.GET.get("end")
        if start_date and end_date:
            try:
                start = datetime.fromisoformat(start_date)
                end = datetime.fromisoformat(end_date)
                events = events.filter(start_date__gte=start, end_date__lte=end)
            except ValueError:
                return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)

        exhibition_type = request.GET.get("exhibition_type")
        if exhibition_type:
            events = events.filter(
                eventtypes__exhibition_type__name__iexact=exhibition_type
            )

        if self.get_bool_param(request, 'upcoming'):
            events = events.filter(start_date__gt=timezone.now())

        if self.get_bool_param(request, 'popular'):
            events = events.annotate(bookmark_count=Count('bookmark')).order_by('-bookmark_count')

        serialized = EventSerializer(events, many=True).data
        return self.api_response(success=True, message="Success", data=serialized, status_code=status.HTTP_200_OK)

    def filter_nearby_locations(self, latitude, longitude, delta=0.10):
        return Location.objects.filter(
            latitude__range=(latitude - delta, latitude + delta),
            longitude__range=(longitude - delta, longitude + delta),
        )