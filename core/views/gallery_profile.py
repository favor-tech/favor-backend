import json
from .base_views import GenericAPIView, Response, IsAuthenticated
from .auth import IsGuestTokenOrAuthenticated
from core.models import *
from django.http import JsonResponse
from core.utils.mixins import ApiResponseMixin
from rest_framework import status

class GalleryProfileView(GenericAPIView, ApiResponseMixin):
    permission_classes = [IsGuestTokenOrAuthenticated]
    #permission_classes = [IsAuthenticated]

    def get(self, request):
        gallery_id = request.GET.get('gallery')

        if not gallery_id:
            return JsonResponse({'error': 'Gallery ID is required.'}, status=400)

        try:
            gallery = Gallery.objects.get(id=gallery_id)
            serialized = GallerySerializer(gallery).data
            return self.api_response(success=True, message="Success", data=serialized, status_code=status.HTTP_200_OK)

        except Gallery.DoesNotExist:
            return JsonResponse({'error': 'Gallery not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)