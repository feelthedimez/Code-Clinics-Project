from calendar_setup.calendar_service import *
from bookings.processing_data import *
from termcolor import colored
from datetime import datetime, timedelta
from dateutil import parser


def is_booking_valid(id):
    """This function checks if this booking is valid and returns a boolean."""

    now = datetime.now()
    data = load_data()
    
    slot = None
    for item in data:
        if id == item[5]:
            slot = item
            break

    if slot == None:
        print(colored("Slot does not exist.", "red"))
        return False
    else:
        user_email = get_user()[0]
        date = parser.parse(slot[0] + " " + slot[1]) - timedelta(minutes=30)

        if slot[4].get('email') == user_email:
            print("\nVolunteer cannot book their own slot.")
            return False
        elif date < now:
            print("\nCannot book 30 min before session.\n")
            return False
        elif slot[3] != "-":
            print("\nSlot is already booked.\n")
            return False         

    return True


def book():
    """This function books a volunteer slot if its available."""

    service = get_service()
    
    if len(sys.argv) != 3:
        command = ""
        for arg in sys.argv[1:]:
            command += f"{arg} "
        print(f"\nUnrecognized command: \"wtc-cal {command.strip()}\"\n")
    else:
        id = sys.argv[2]

        if is_booking_valid(id):
            event = service.events().get(calendarId='wtcteam19jhb@gmail.com', 
            maxAttendees = 1, eventId=id).execute()
            
            volunteer = event['creator'].get('email')
            event['status'] = 'confirmed'
            attendee = get_user()[0]

            event['attendees'] = [
                {
                    "email": attendee,
                },
                {
                    "email": volunteer + "not"
                }
            ]

            update_event = service.events().update(
                calendarId='wtcteam19jhb@gmail.com',
                eventId=event["id"], body=event).execute()

            summary = event['summary']
            volunteer = event['creator'].get('email')
            start = parser.parse(event['start'].get('dateTime'))
            time = start.strftime("%H:%M:%S")
            date = start.strftime("%Y-%m-%d")

            booking_summary(summary, volunteer, time, date)
        else:
            msg = colored("FAILED!", "red")
            print(f"Booking {msg}")   


def booking_summary(summary, volunteer, time, date):
    """This will print out the booking details in a summarised format."""

    msg = colored("BOOKING CONFIRMED:", "green")
    print(f"\n{msg}\n")
    print(f"  Booking Summary")
    print(f"  Summary: {summary}")
    print(f"  Instructor: {volunteer}")
    print(f"  Time: {time}")
    print(f"  Date: {date}\n\n")