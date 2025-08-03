from .base_views import GenericAPIView, Response, IsAuthenticated
from core.models import *




class GalleryView(GenericAPIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        galleries = Gallery.objects.filter()
        serialized = GallerySerializer(galleries, many=True).data
        return Response(serialized, status=200)

