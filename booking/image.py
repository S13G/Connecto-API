import os
from datetime import datetime


def get_media_paths(request, filename):
    original_filename = filename
    nowTime = datetime.now().strftime('%Y_%m_%d_%H:%M:%S_')
    filename = "%s%s%s" % ('vehicle_', nowTime, original_filename)

    return os.path.join('vehicle_collections/', filename)