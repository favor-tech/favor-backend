from .base_views import GenericAPIView, Response, IsAuthenticated
from core.models import *
from django.http import JsonResponse
import json
from core.utils.mixins import ApiResponseMixin
from rest_framework import status


class UserProfileView(GenericAPIView, ApiResponseMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id

        try:
            user = User.objects.get(id=user_id)
            serialized = UserSerializer(user).data
            return self.api_response(success=True, message="Success", data=serialized, status_code=status.HTTP_200_OK)

        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

