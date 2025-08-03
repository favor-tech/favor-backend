from .base_views import GenericAPIView, Response, IsAuthenticated
from core.models import *
from django.http import JsonResponse
from core.utils.mixins import ApiResponseMixin
from rest_framework import status

class BookmarkView(GenericAPIView, ApiResponseMixin):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            event_id = request.data.get("event")
            event = Event.objects.get(id=event_id)

            bookmark = Bookmark.objects.filter(user=user, event=event).first()

            if bookmark:
                bookmark.delete()
                return self.api_response(
                    success=True,
                    message="Bookmark removed",
                    data={"is_bookmarked": False},
                    status_code=status.HTTP_200_OK
                )
            else:
                new_bookmark = Bookmark.objects.create(user=user, event=event)
                serialized = BookmarkSerializer(new_bookmark, context={"request": request})
                return self.api_response(
                    success=True,
                    message="Bookmark added",
                    data={**serialized.data, "is_bookmarked": True},
                    status_code=status.HTTP_201_CREATED
                )
        except Event.DoesNotExist:
            return self.api_response(
                success=False,
                message="Event not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return self.api_response(
                success=False,
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )
