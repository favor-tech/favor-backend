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


######## THIS WILL BE USED IN THE GLOBAL SCENARIO #############

# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from core.models import GalleryLocation
# from core.utils.location_utils import get_or_create_location_from_latlon

# @receiver(pre_save, sender=GalleryLocation)
# def autofill_location_from_coordinates(sender, instance, **kwargs):
#     if instance.latitude and instance.longitude:
#         if not instance.province or not instance.district:
#             matched_location = get_or_create_location_from_latlon(instance.latitude, instance.longitude)
#             if matched_location:
#                 if not instance.province:
#                     instance.province = matched_location.province
#                 if not instance.district:
#                     instance.district = matched_location.district
#                 if not instance.city:
#                     instance.city = matched_location.city
#                 if not instance.country:
#                     instance.country = matched_location.country
