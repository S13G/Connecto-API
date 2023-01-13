import json

import requests
from decouple import config

from booking.models import Country, Place

url = "https://api.duffel.com/air/airports"
api_key = config('API_KEY')

headers = {
    "Authorization": "Bearer " + api_key,
    "Duffel-Version": "beta",
    "version": "0.3",
    "Content-Type": "application/json"
}

params = {
    "limit": 50,
}

response = requests.get(url=url, headers=headers, params=params)
json_obj = response.text
result = json.loads(json_obj)

for i in range(50):
    data = result["data"][i]
    # values_list = Country.objects.all().values_list("code", flat=True)
    iata_code = data["iata_country_code"]
    # iata_country = Country.objects.get(code=data["iata_country_code"])
    country, created = Country.objects.get_or_create(code=iata_code)
    # if data["iata_country_code"] in values_list:
    Place.objects.create(name=data["name"], country=country,
                         category="Airport", code=data["iata_code"], longitude=data["longitude"],
                         latitude=data["latitude"])
else:
    pass
