from .base_views import GenericAPIView, Response, IsAuthenticated
from .auth import IsGuestTokenOrAuthenticated
from core.models import Event, GalleryLocation, EventSerializer , Location
from core.utils.mixins import ApiResponseMixin
from core.utils.location_utils import haversine 
from rest_framework import status
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime

class EventsView(GenericAPIView, ApiResponseMixin):
    permission_classes = [IsGuestTokenOrAuthenticated]

    def get(self, request):
        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')
        is_free = request.GET.get('is_free')

        if is_free:
            is_free = is_free.lower() == 'true'
        else:
            is_free = None

        if not latitude or not longitude:
            return self.api_response(
                success=False,
                message="Latitude and longitude are required.",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            return self.api_response(
                success=False,
                message="Invalid latitude or longitude format.",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        use_province_filter = True #self.get_bool_param(request, 'upcoming') or self.get_bool_param(request, 'popular')

        if use_province_filter:
            try:
                ### THESE 2 LINES WILL BE USE INSTEAD OF BELOW LINE , IN THE GLOBAL SCENARIO ###
                #from core.utils.location_utils import get_or_create_location
                #matched_location = get_or_create_location(latitude, longitude)

                matched_location = Location.objects.filter(
                    latitude__range=(latitude - 0.1, latitude + 0.1),
                    longitude__range=(longitude - 0.1, longitude + 0.1),
                ).first()

                if matched_location and matched_location.province:
                    province_name = matched_location.province
                    nearby_locations = GalleryLocation.objects.filter(
                        province__iexact=province_name
                    )
                else:
                    nearby_locations = self.filter_nearby_locations(latitude, longitude)

            except Exception:
                nearby_locations = self.filter_nearby_locations(latitude, longitude)
        else:
            nearby_locations = self.filter_nearby_locations(latitude, longitude)

        events = Event.objects.filter(
            gallery_location__in=nearby_locations,
            is_active=True
        )

        if is_free is not None:
            events = events.filter(is_free=is_free)

        start_date = request.GET.get("start")
        end_date = request.GET.get("end")
        if start_date and end_date:
            try:
                start = datetime.fromisoformat(start_date)
                end = datetime.fromisoformat(end_date)
                events = events.filter(
                    Q(is_indefinite=True) |
                    Q(start_date__gte=start, end_date__lte=end, is_indefinite=False)
                )
            except ValueError:
                return self.api_response(
                    success=False,
                    message="Invalid date format. Use YYYY-MM-DD.",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
        else:
            today = timezone.now()
            events = events.filter(
                Q(is_indefinite=True) |
                Q(end_date__gte=today, is_indefinite=False)
            )

        exhibition_type = request.GET.get("exhibition_type")
        if exhibition_type:
            events = events.filter(
                eventtypes__exhibition_type__name__iexact=exhibition_type
            )

        if self.get_bool_param(request, 'upcoming'):
            now = timezone.now()
            events = events.filter(
                Q(is_indefinite=True) |
                Q(start_date__gt=now, is_indefinite=False)
            )
        if self.get_bool_param(request, 'popular'):
            events = events.annotate(bookmark_count=Count('bookmark')).order_by('-bookmark_count')
        else:
            event_distance_pairs = []
            for event in events:
                location = event.gallery_location
                if location:
                    distance = haversine(latitude, longitude, location.latitude, location.longitude)
                    event_distance_pairs.append((distance, event))

            event_distance_pairs.sort(key=lambda x: x[0])
            events = [pair[1] for pair in event_distance_pairs]


        serialized = EventSerializer(events, many=True, context={"request": request}).data
        return self.api_response(
            success=True,
            message="Success",
            data=serialized,
            status_code=status.HTTP_200_OK
        )
    def filter_nearby_locations(self, latitude, longitude, delta=0.2):
        return GalleryLocation.objects.filter(
            latitude__range=(latitude - delta, latitude + delta),
            longitude__range=(longitude - delta, longitude + delta),
        )
