import json
from .base_views import GenericAPIView, Response, IsAuthenticated
from .auth import IsGuestTokenOrAuthenticated
from core.models import *
from django.http import JsonResponse
from core.utils.mixins import ApiResponseMixin
from rest_framework import status

class ArtistProfileView(GenericAPIView, ApiResponseMixin):
    permission_classes = [IsGuestTokenOrAuthenticated]
    #permission_classes = [IsAuthenticated]

    def get(self, request):
        artist_id = request.GET.get('artist')

        if not artist_id:
            return JsonResponse({'error': 'Artist ID is required.'}, status=400)

        try:
            artist = Artist.objects.get(id=artist_id)
            serialized = ArtistSerializer(artist).data
            return self.api_response(success=True, message="Success", data=serialized, status_code=status.HTTP_200_OK)

        except Artist.DoesNotExist:
            return JsonResponse({'error': 'Artist not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)