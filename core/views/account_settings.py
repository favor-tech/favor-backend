from .base_views import GenericAPIView, Response, IsAuthenticated
from core.models import User,UserSerializer
from core.utils.mixins import ApiResponseMixin
from rest_framework import status

class AccountSettingsView(GenericAPIView, ApiResponseMixin):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            user.name = request.data.get("name")
            user.surname = request.data.get("surname")
            user.about = request.data.get("about")

            if "profile_picture" in request.FILES:
                user.profile_picture = request.FILES["profile_picture"]

            user.save()

            return self.api_response(
                success=True,
                message="Success",
                data=UserSerializer(user).data,
                status_code=status.HTTP_200_OK
            )
        except Exception as e:
            return self.api_response(
                success=False,
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )
