from dal import autocomplete
from django import forms
from .models import Event, GalleryLocation

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        widgets = {
            "gallery_location": autocomplete.ModelSelect2(
                url='gallerylocation-autocomplete',
                forward=['gallery']
            )
        }