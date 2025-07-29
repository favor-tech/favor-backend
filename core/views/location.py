from core.models import Location
from .base_views import GenericAPIView, Response
from .auth import IsGuestTokenOrAuthenticated
from core.utils.mixins import ApiResponseMixin
from django.core.cache import cache
from rest_framework import status


class LocationProvinceDistrictView(GenericAPIView, ApiResponseMixin):
    permission_classes = [IsGuestTokenOrAuthenticated]

    def get(self, request):
        CACHE_KEY = "location_province_districts_v2"
        VERSION = "2.0.0"

        cached_data = cache.get(CACHE_KEY)
        if cached_data:
            return self.api_response(
                success=True,
                message="Success (from cache)",
                data={
                    "version": VERSION,
                    "locations": cached_data
                },
                status_code=status.HTTP_200_OK
            )

        raw_data = Location.objects.filter(
            province__isnull=False,
            district__isnull=False
        ).values("province", "district", "latitude", "longitude")

        result = {}

        for row in raw_data:
            province = row["province"]
            district = row["district"]
            lat = row["latitude"]
            lon = row["longitude"]

            if province and district:
                result.setdefault(province, [])
                result[province].append({
                    "district": district,
                    "latitude": lat,
                    "longitude": lon
                })

        structured_data = [
            {
                "province": province,
                "districts": sorted(districts, key=lambda x: x["district"])
            }
            for province, districts in sorted(result.items())
        ]

        cache.set(CACHE_KEY, structured_data, timeout=60 * 60 * 24)

        return self.api_response(
            success=True,
            message="Success",
            data={
                "version": VERSION,
                "locations": structured_data
            },
            status_code=status.HTTP_200_OK
        )
