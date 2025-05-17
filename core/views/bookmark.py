from .base_views import GenericAPIView, Response, IsAuthenticated
from core.models import *
from django.http import JsonResponse
import json
from core.utils.mixins import ApiResponseMixin
from rest_framework import status

class BookmarkView(GenericAPIView,ApiResponseMixin):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            event_id = request.data.get("event_id")
            event = Event.objects.get(id=event_id)
            bookmark = Bookmark.objects.create(user=user, event=event)
            return self.api_response(success=True,message="Success",data=bookmark,status_code=status.HTTP_200_OK)
        except Exception as e:
            return self.api_response(success=False,message=str(e),status_code=status.HTTP_400_BAD_REQUEST)