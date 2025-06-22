from .base_views import GenericAPIView, Response, IsAuthenticated
from core.models import *
from django.http import JsonResponse
import json
from core.utils.mixins import ApiResponseMixin
from rest_framework import status

from core.models import Bookmark

class BookmarkListView(GenericAPIView, ApiResponseMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        bookmarks = user.app_bookmark.select_related("event").all()

        event_list = []
        for bookmark in bookmarks:
            event_data = EventMiniSerializer(bookmark.event, context={"request": request}).data
            event_list.append({
                "event": event_data,
                "bookmarked_at": bookmark.bookmarked_at
            })
        return Response({
            "success": True,
            "message": "Success",
            "user": UserMiniSerializer(user).data,
            "data": event_list
        }, status=status.HTTP_200_OK)
