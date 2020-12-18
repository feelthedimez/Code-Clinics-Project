from calendar_setup.calendar_service import *
import ics
from icalendar import Calendar, Event, vCalAddress
import sys
import re
import datetime as dt
from datetime import datetime, timedelta
from dateutil import parser
import json
from termcolor import colored


cal = Calendar()


def get_user():
    """This function returns the user email and user name."""

    user_details = None

    config_path = f"{sys.path[0]}/files/json/.config.json"
    with open(config_path, 'r') as json_file:
        user_details = json.load(json_file)

    user_email = user_details.get('email')
    user_name = user_email.split("@")[0]

    return user_email, user_name


def cancel():
    """This function cancels a booking."""

    now = datetime.now()

    if len(sys.argv) != 3:
        command = ""
        for arg in sys.argv[1:]:
            command += f"{arg} "
        print(f"\nUnrecognized command: \"wtc-cal {command.strip()}\"\n")
    else:
        data = load_data()
        id = sys.argv[2]

        slot = None
        for item in data:
            if id == item[5]:
                slot = item
                break

        if slot == None:
            print(colored("Slot does not exist.", "red"))
        else:
            user_email = get_user()[0]
            
            if user_email == slot[3]:
                delete_booking(slot, now)
            elif user_email == slot[4].get('email'):
                delete_slot(slot)
            else:
                print("Cancellation Failed")


def delete_slot(slot):
    """This function deletes the volunteer slot / deletes the event."""

    service = get_service()

    if slot[3] == "-":
        id = slot[5]

        event = service.events().delete(calendarId='wtcteam19jhb@gmail.com',
        eventId=id).execute()
        print("Event cancelled!")
    else:
        print("Cancellation Failed. \n\n - Patient has already booked\n")


def delete_booking(slot, now):
    """This function deletes the booked slot/deletes the booking."""

    service = get_service()

    # Booking start time and End time
    start = parser.parse(slot[0] + " " + slot[1])
    end = start + timedelta(minutes=30)

    # Get date now and booking date
    date_now = now.date()
    date_slot = start.date()

    # Get time now and booking start date 15 minutes prior
    start = start - timedelta(minutes=15)
    time_slot = start.time()
    time_now = now.time()
    user_email = get_user()[0]

    # Compare date and time objects
    if date_now == date_slot and time_slot <= time_now:
        print("\nCannot cancel 15min befor session!\n")
    else:
        id = slot[5]
        event = service.events().get(calendarId='wtcteam19jhb@gmail.com', 
            eventId=id).execute()

        event['status'] = 'tentative'
        event['attendees'] = []

        update_event = service.events().update(
            calendarId='wtcteam19jhb@gmail.com',
            eventId=event['id'], body=event).execute()

        print("Booking is canceled")


def save_data(data):
    """This function saves the code clinics data to a local file."""

    old_data = load_data()

    file_path = f"{sys.path[0]}/files/json/data.json" 
    if data != old_data:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        save_to_ics(data)


def load_data():
    """This function loads the code clinics data to a local file."""

    data = None

    file_path = f"{sys.path[0]}/files/json/data.json" 
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except:
        pass

    return data


def save_to_ics(data):
    """This function converts .json data file to a .ics file format and saves it.
    """

    for e in data:
        start = datetime.fromisoformat(e[0] + "T" + e[1] + "+02:00")
        end = start + timedelta(minutes=30)
        email = e[4].get('email')
        organizer = vCalAddress(f"MAILTO:{email}")

        status = "CONFIRMED"        
        if e[6] == "[OPEN}]":
            status = "TENTATIVE"

        event = Event()
    
        event.add('summary', e[2])
        event.add('dtstart', start)
        event.add('dtend', end)
        event.add('description', e[7])
        event.add('organizer', organizer)
        event.add('STATUS', status)
        event.add('uid', e[5])
        if e[3] != "":
            attendee = vCalAddress(f"MAILTO:{e[3]}")
            event.add('attendee', attendee)
            
        cal.add_component(event)

    file_path = f"{sys.path[0]}/files/ics/data.ics" 

    with open(file_path, 'wb') as file:
        file.write(cal.to_ical())


