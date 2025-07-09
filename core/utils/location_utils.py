from math import radians, cos, sin, asin, sqrt
from core.models import Location

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

def get_closest_location(lat, lon, delta=0.2):
    candidates = Location.objects.filter(
        latitude__range=(lat - delta, lat + delta),
        longitude__range=(lon - delta, lon + delta)
    )
    if not candidates.exists():
        return None

    closest = min(
        candidates,
        key=lambda loc: haversine(lat, lon, loc.latitude, loc.longitude)
    )
    return closest
