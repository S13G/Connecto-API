from background_task import background

from booking.emails import Util
from booking.models import Booking


@background(schedule=60)
def transport_reminder(booking_id):
    booking = Booking.objects.get(id=booking_id)
    Util.remind_booker(booking)
