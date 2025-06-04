from dal import autocomplete
from core.models import GalleryLocation

class GalleryLocationAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = GalleryLocation.objects.all()

        gallery_id = self.forwarded.get('gallery', None)
        if gallery_id:
            qs = qs.filter(gallery_id=gallery_id)
        else:
            qs = qs.none()

        return qs