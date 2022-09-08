from decouple import config
from urllib import response
from booking.models import Place, Country

import json
import requests

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
    if data["iata_country_code"] == Country.objects.all().values_list("code"):
        Place.objects.create(name=data["name"], country=data["iata_country_code"],
                             category='Airport', code=data["iata_code"], longitude=data["longitude"],
                             latitude=data["latitude"])
    else:
        pass
