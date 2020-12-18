from random import randint
from calendar_setup.calendar_service import *
from prettytable import PrettyTable
from termcolor import colored
from dateutil import parser
from bookings.processing_data import *
import json
import sys
from datetime import datetime, timedelta
from dateutil import parser


def show_calendars(prompt=None):
    """This will get all the available slots form the WTC calendar."""

    
    if prompt == "primary":
        user_name = get_user()[1] 
        print(f"\n{user_name.title()} Calendar")
        print_slots(get_primary_calendar())
    elif prompt == None:
        print("\nCode Clinics Calendar")
        print_slots(get_code_clinics_calendar())
    
    else:
        command = sys.argv[1]
        if (len(sys.argv) == 3 and (command == 'slots' or command == "my_cal")
            and sys.argv[2].isdigit()):
            get_time_constraints(int(sys.argv[2]))
        else:
            command = ""
            for arg in sys.argv[1:]:
                command += f"{arg} "
            print(f"Unrecognized command: \"wtc-cal {command.strip()}\"")


def print_slots(data):
    """This function will print out the calendars - for both student and calendar
    slots."""

    date = colored("DATE", 'green')
    time = colored("TIME", 'green')
    summary = colored("SUMMARY", 'cyan')
    volunteer = colored("VOLUNTEER", 'red')
    creator = colored("CREATOR", 'red')
    patient = colored("PATIENT", "magenta")
    id = colored("ID", "yellow")

    table = PrettyTable()

    if data != []:

        if len(data[0]) == 4:
            table.field_names = [date, time, summary, creator]
        else:
            table.field_names = [date, time, summary, patient, 
                                volunteer, id, "STATUS"]
            data = formatted_data_output(data)
    
        for entry in data:
            table.add_row(entry)
        print(table)
    else:
        print("There are no upcoming events.")
        print("   Run 'wtc-cal volunteer' to create a slot!")


def formatted_data_output(data):
    """This function formats the data to add color to some content when it will be
    printed out and returns the formated data."""

    print_data = []

    # Data for STUDENT CALENDAR
    if len(data[0]) == 5:
        for item in data:
            # Make the summary limited to 12 characters if it exceeds 15
            info = item[2]
            event_summary = f"{info[:12]}..." if len(info) > 15 else info
            slot = [item[0], item[1], event_summary, item[3], item[4]]

            print_data.append(slot)
            
        return print_data

    # Data for SLOTS CALENDAR
    for item in data:
        # Make the summary limited to 12 characters if it exceeds 15
        info = item[2]
        event_summary = f"{info[:12]}..." if len(info) > 15 else info

        # Display just the user name instead of user email of the volunteer
        volunteer = item[4].get('email').split("@")[0]

        # Display just the user name instead of user email of the patient
        patient = item[3]
        if patient != "":
            patient = item[3].split("@")[0]
        else:
            patient = item[3]

        if item[6] == "[OPEN]":
            status = colored("[OPEN]", "cyan")
        elif item[6] == "[BOOKED]":
            status = colored("[BOOKED]", "red")

        slot = [item[0], item[1], event_summary, patient, volunteer, item[5],
                status]

        print_data.append(slot)
    
    return print_data


def get_date_and_time(date_time):
    """This function takes a datetime object and returns a seperate date and time
    strings."""

    date_time = parser.parse(date_time)
    time = date_time.strftime("%H:%M:%S")
    date = date_time.strftime("%Y-%m-%d")

    return date, time


def get_code_clinics_calendar():
    """This function returns the code-clinics calendar."""

    events_results = get_events_results('wtcteam19jhb@gmail.com')
    events = events_results.get('items', [])

    data = []
    if not events:
        pass
    
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        date, time = get_date_and_time(start)

        if event['status'] == 'tentative':
            status = "[OPEN]"
            patient = "-"
        elif event['status'] == 'confirmed':
            status = "[BOOKED]"
            patient = event['attendees'][0]['email']

        data.append([date, time, event['summary'], patient, event['creator'],
                    event['id'], status, event.get('description')])

    return data


def get_primary_calendar():
    """This function returns the primary calendar (user calendar)."""

    events_results = get_events_results()
    events = events_results.get('items', [])

    data = []
    if not events:
        pass

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        date, time = get_date_and_time(start)
         
        email = ""
        while True:
            email = event['creator'].get('email')
            if email.find("not") < 0:
                break

        data.append([date, time, event['summary'], 
            email])
     
    return data


def slot_details():
    """This function list details of the specified slot (Booking or Volunteering).
    """
    
    if len(sys.argv) != 3:
        command = ""
        for arg in sys.argv[1:]:
            command += f"{arg} "
        print(f"Unrecognized command: \"wtc-cal {command.strip()}\"")
    else:
        id = sys.argv[2].strip()
        data = load_data()
    
        slot = None
        for item in data:
            if id == item[5]:
                slot = item
                break

        if slot == None:
            print(colored("Slot does not exist.", "red"))
        else:
            date = parser.parse(slot[0] +" "+ slot[1]) + timedelta(minutes=30)
            end = date.strftime("%H:%M")

            msg = colored("Slot details:", "yellow")
            print(f"\n{msg} {colored(item[5], 'yellow')}\n")
            print("  Creator:\t", item[4].get('email'))
            print("  Attendee:\t", item[3])
            print("  Summary:\t", item[2])
            print("  Description:\t", item[7])
            print("  Date:\t\t", slot[0])
            print(f"  Time:\t\t {slot[1][:5]} - {end}\n")