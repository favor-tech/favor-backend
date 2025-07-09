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


##### FUNCTION THAT WILL BE USED IN GLOBAL SCENARIO TO GET PROVINCE AND DISTRICT FROM DIRECTLY USER #####

'''
import requests

def get_or_create_location_from_latlon(user_lat, user_lon):
    candidates = Location.objects.filter(
        latitude__range=(user_lat - 0.2, user_lat + 0.2),
        longitude__range=(user_lon - 0.2, user_lon + 0.2)
    )

    if candidates.exists():
        closest = min(candidates, key=lambda loc: haversine(user_lat, user_lon, loc.latitude, loc.longitude))
        return closest

    try:
        # 1. Get city information with Reverse Geocode
        reverse_resp = requests.get(
            'https://nominatim.openstreetmap.org/reverse',
            params={
                'format': 'jsonv2',
                'lat': user_lat,
                'lon': user_lon,
                'zoom': 10,
                'addressdetails': 1
            },
            headers={'User-Agent': 'your-app-name/1.0'}
        )
        if reverse_resp.status_code != 200:
            return None

        reverse_data = reverse_resp.json()
        addr = reverse_data.get("address", {})
        city = addr.get("city") or addr.get("town") or addr.get("village")
        province = addr.get("state")
        country = addr.get("country")
        district = addr.get("county") or addr.get("suburb")

        if not city:
            return None

        # 2. Get city center coordinates (forward geocode)
        forward_resp = requests.get(
            'https://nominatim.openstreetmap.org/search',
            params={
                'q': city,
                'format': 'json',
                'limit': 1,
                'country': country
            },
            headers={'User-Agent': 'your-app-name/1.0'}
        )
        if forward_resp.status_code != 200 or not forward_resp.json():
            return None

        forward_data = forward_resp.json()[0]
        center_lat = float(forward_data['lat'])
        center_lon = float(forward_data['lon'])

        # 3. New record in the Location table
        location = Location.objects.create(
            latitude=center_lat,
            longitude=center_lon,
            city=city,
            province=province,
            country=country,
            district=district,
            region=addr.get('region'),
        )
        return location

    except Exception as e:
        print("❌ Geocoding failed:", e)
        return None
'''