import json

from booking.models import Place, Country

with open('worldcities.json') as json_file:
    data = json.load(json_file)
    for p in data:
        # create YourModel object and save it to database
        values_list = Country.objects.all().values_list("code", flat=True)
        iso_country = Country.objects.get(code=p["iso2"])
        if p["iso2"] in values_list:
            Place.objects.create(name=p['city'], country=iso_country, category='City',
                                 code=p['iso2'], longitude=p['lng'], latitude=p['lat'])
        else:
            pass
