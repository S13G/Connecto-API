from __future__ import unicode_literals

import json

from django.db import migrations


def load_file(apps, schema_editor):
    Country = apps.get_model('booking', 'Country')

    with open('json_dir/countries.json') as json_file:
        data = json.load(json_file)
        for p in data:
            # create YourModel object and save it to database
            country = Country.objects.create(name=p['name'], code=p['code'])


class Migration(migrations.Migration):
    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_file, None)
    ]
