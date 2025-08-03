from .base_views import GenericAPIView, Response, IsAuthenticated
from core.models import UserLocation, Location
from core.utils.mixins import ApiResponseMixin
from django.utils import timezone
from rest_framework import status

class UserLocationCreateView(GenericAPIView, ApiResponseMixin):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        province = request.data.get("province")
        district = request.data.get("district")
        selected = request.data.get("selected", None)

        if not province or not district:
            return self.api_response(
                success=False,
                message="Both province and district are required.",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            location = Location.objects.get(
                province__iexact=province.strip(),
                district__iexact=district.strip()
            )
        except Location.DoesNotExist:
            return self.api_response(
                success=False,
                message="Matching location not found.",
                status_code=status.HTTP_404_NOT_FOUND
            )

        selected_flag = bool(selected) if selected is not None else False

        UserLocation.objects.filter(user=user).update(is_active=False)

        existing = UserLocation.objects.filter(
            user=user,
            location=location,
            selected=selected_flag
        ).first()

        if existing:
            existing.detected_at = timezone.now()
            existing.updated_at = timezone.now()
            existing.is_active = True
            existing.save()
            result = "updated"
        else:
            UserLocation.objects.create(
                user=user,
                location=location,
                detected_at=timezone.now(),
                is_active=True,
                selected=selected_flag
            )
            result = "created"

        return self.api_response(
            success=True,
            message=f"Location {result} successfully.",
            status_code=status.HTTP_200_OK
        )

class UserLocationListView(GenericAPIView, ApiResponseMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        limit = request.GET.get("limit", 10)

        try:
            limit = int(limit)
        except ValueError:
            return self.api_response(
                success=False,
                message="Limit must be an integer.",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        locations = UserLocation.objects.filter(user=user).order_by(
            "-updated_at", "-detected_at"
        )[:limit]

        data = [
            {
                "province": loc.location.province,
                "district": loc.location.district,
                "latitude": loc.location.latitude,
                "longitude": loc.location.longitude,
                "detected_at": loc.detected_at,
                "selected": loc.selected,
                "is_active": loc.is_active,
            }
            for loc in locations
        ]

        return self.api_response(
            success=True,
            message="User location history",
            data=data,
            status_code=status.HTTP_200_OK
        )