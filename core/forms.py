from dal import autocomplete
from django import forms
from .models import Event , GalleryLocation
from datetime import datetime,date
from django.utils import timezone

class EventForm(forms.ModelForm):
    start_date = forms.DateTimeField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        input_formats=['%Y-%m-%d'],
    )
    end_date = forms.DateTimeField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        input_formats=['%Y-%m-%d'],
    )

    class Meta:
        model = Event
        fields = "__all__"
        widgets = {
            "gallery_location": autocomplete.ModelSelect2(
                url='gallerylocation-autocomplete',
                forward=['gallery']
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["start_date"].input_formats = ["%Y-%m-%d"]
        self.fields["end_date"].input_formats = ["%Y-%m-%d"]
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
    
        if db_field.name == "gallery_location":
            if request._obj_ is not None:
                kwargs["queryset"] = GalleryLocation.objects.filter(gallery=request._obj_.gallery)
            else:
                kwargs["queryset"] = GalleryLocation.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


    def get_form(self, request, obj=None, **kwargs):
        request._obj_ = obj
        return super().get_form(request, obj, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        is_indefinite = cleaned_data.get("is_indefinite")
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and isinstance(start_date, date):
            cleaned_data["start_date"] = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))

        if end_date and isinstance(end_date, date):
            cleaned_data["end_date"] = timezone.make_aware(datetime.combine(end_date, datetime.min.time()))

        if not is_indefinite:
            if not cleaned_data.get("start_date"):
                self.add_error("start_date", "Süreli etkinlikler için başlangıç tarihi zorunludur.")
            if not cleaned_data.get("end_date"):
                self.add_error("end_date", "Süreli etkinlikler için bitiş tarihi zorunludur.")
        else:
            if cleaned_data.get("start_date"):
                self.add_error("start_date", "Süresiz etkinliklerde başlangıç tarihi girilmemelidir.")
            if cleaned_data.get("end_date"):
                self.add_error("end_date", "Süresiz etkinliklerde bitiş tarihi girilmemelidir.")

        return cleaned_data

