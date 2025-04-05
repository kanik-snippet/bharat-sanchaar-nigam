import requests
import time
import json
from django.core.management.base import BaseCommand
from news.models import District  # Adjust the import based on your model location

# Replace with your actual API Key
LOCATIONIQ_API_KEY = "pk.f6f9c5d0d4f3f177eb8d80ba23433e05"

# Function to fetch latitude, longitude, and polygon from LocationIQ
def get_location_data(place_name, country="India"):
    base_url = "https://us1.locationiq.com/v1/search.php"
    params = {
        "key": LOCATIONIQ_API_KEY,
        "q": f"{place_name}, {country}",
        "format": "json",
        "polygon_geojson": 1  # Request polygon data
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        data = response.json()

        if not data:
            print(f"⚠️ No data found for {place_name}")
            return None, None, None

        latitude = float(data[0].get("lat", 0))
        longitude = float(data[0].get("lon", 0))
        polygon = data[0].get("geojson", {}).get("coordinates", None)

        if latitude == 0 and longitude == 0:
            print(f"⚠️ Invalid coordinates received for {place_name}")
            return None, None, None

        return latitude, longitude, polygon

    except requests.exceptions.RequestException as e:
        print(f"❌ API request failed for {place_name}: {e}")
        return None, None, None
    except (KeyError, ValueError, IndexError) as e:
        print(f"❌ Data parsing error for {place_name}: {e}")
        return None, None, None

# Django command to update all district locations
class Command(BaseCommand):
    help = "Fetch and update latitude, longitude, and polygon for all districts"

    def handle(self, *args, **kwargs):
        districts = District.objects.filter(latitude__isnull=True, longitude__isnull=True)

        if not districts.exists():
            print("✅ All districts already have location data.")
            return

        for district in districts:
            print(f"📍 Fetching location for: {district.name}")
            latitude, longitude, polygon = get_location_data(district.name)

            if latitude and longitude:
                district.latitude = latitude
                district.longitude = longitude
                district.polygon = json.dumps(polygon) if polygon else None
                district.save()
                print(f"✅ Updated {district.name}: ({latitude}, {longitude})")
            else:
                print(f"⚠️ Skipped {district.name} (No valid data found)")

        print("🎯 District locations updated successfully!")
