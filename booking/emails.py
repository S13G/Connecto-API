import threading

from django.core.mail import EmailMessage
from django.template.loader import render_to_string


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def success_booking_email(booking):
        subject = "Booking Successful"
        message = render_to_string('booking_email.html', {
            'first_name': booking.first_name,
            'last_name': booking.last_name,
            'vehicle': booking.vehicle.vehicle_make_and_model,
            'from_place': booking.from_place.name,
            'to_place': booking.to_place.name,
            'passengers': booking.passengers,
            'date': booking.departure,
        })

        msg = EmailMessage(subject=subject, body=message, to=[booking.email_address])
        msg.content_subtype = "html"
        EmailThread(msg).start()

    @staticmethod
    def remind_booker(booking):
        subject = "Transport Reminder"
        message = render_to_string('reminder_email.html', {
            'first_name': booking.first_name,
            'last_name': booking.last_name,
            'date': booking.departure,
        })

        msg = EmailMessage(subject=subject, body=message, to=[booking.email_address])
        msg.content_subtype = "html"
        EmailThread(msg).start()
