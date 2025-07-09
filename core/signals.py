from django.db.models.signals import pre_save
from django.dispatch import receiver
from core.models import GalleryLocation
from core.utils.location_utils import get_closest_location

@receiver(pre_save, sender=GalleryLocation)
def autofill_province_from_coordinates(sender, instance, **kwargs):
    if instance.latitude and instance.longitude:
        # Fill Province and District automatically
        if not instance.province or not instance.district:
            closest = get_closest_location(instance.latitude, instance.longitude)
            if closest:
                if not instance.province:
                    instance.province = closest.province
                if not instance.district:
                    instance.district = closest.district
