from calendar_setup.calendar_service import *
from bookings.processing_data import *
import sys
import re
import random
import datetime as dt
from datetime import datetime, timedelta
from dateutil import parser
import json
from termcolor import colored


def weekdays(day):
    """Printing out days of the week, and returning a dictionary with days of
    the week."""

    week_days = {
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday",
        7: "Sunday"
    }

    return week_days[day]


def volunteer():
    """This function creates a volunteering slot."""

    user_email, user_name = get_user()
    print(colored(f"{user_name.title()} slot volunteering:", "cyan"))

    dates = {}

    for i in range(7):
        day = dt.date.today() + timedelta(days=i)
        dates[str(day)[-2:]] = day


    print('\nThese are the dates for the next 7 days:\n')

    for v, i in enumerate(dates):
        if v == 0:
            current_day = f" {colored('[Current DAY]', 'yellow')}"
            print('\t' + i, weekdays(dates[i].weekday()+1) + current_day, sep=': ')
        else:  
            print('\t' + i, weekdays(dates[i].weekday()+1), sep=': ')

    if len(sys.argv) != 2:
        command = ""
        for arg in sys.argv[1:]:
            command += f"{arg} "
        print(f"Unrecognized command: \"wtc-cal {command.strip()}\"")
        print("\nUsage:\t\"wtc-cal volunteer [<args>]\"")
    else:
        fail = colored("Failed", "red")
        start, end, summary, description = get_params()

        valid = all(arg != None for arg in [start, end, summary, description])

        if valid == False:
            print(f"\nVolunteering {fail}.")
        elif is_volunteering_valid(start, user_email):
            id = create_event(start, end, summary, description, user_email)
        else:
            print(f"\nVolunteering {fail}.")


def is_volunteering_valid(start, user_email):
    """This function checks if slot does not already exist and returns a boolean.
    """

    data = load_data()
    
    items = []
    for item in data:
        if item[4].get('email') == user_email:
            items.append(item)

    if len(items) > 0:
        
        # Create current start and end datetime object
        start = parser.parse(start)
        end = start + timedelta(minutes=30)
        # Get new volunteer booking date, start-time and end-time
        n_date = start.date()
        n_start_time = start.time()
        n_end_time = end.time()
        
        for slot in items:
            # Get old slot date, start-time
            start = parser.parse(slot[0] +" "+ slot[1])
            end = start + timedelta(minutes=30)
            
            o_date = start.date()
            o_start_time = start.time()
            o_end_time = end.time() 

            # Condition to check if the times do not clash
            time_validation = ((n_end_time <= o_start_time and n_end_time < o_end_time) or 
                (n_start_time >= o_end_time and n_end_time > o_start_time))

            # Condition to check if booking is on the same day and whether the times clash
            date_validation = (n_date == o_date) #and time_validation
            if date_validation:
                if time_validation == False:
                    print("\nDouble booking is not allowed!\n")
                    return False

    return True


def get_date(date):
    """This function gets the event date in the format (YYYY-MM-DD) from the 
    user input and returns a datetime object if correct or error message if not.
    """

    input_date_time = input("\n\n    Enter date (DD): ")
    year = date.split('-')[0]
    month = date.split('-')[1]
    match = re.match("\d\d", input_date_time) is None
    user_date = f'{year} - {month} - {input_date_time}'
 
    if match != None:

        try:
            date_now = parser.parse(date)

            input_date = parser.parse(user_date)
            result = (input_date - date_now).days      
            if result >= 0 and result <= 30:
                return input_date
        except ValueError:
            pass
    
    date_max = (parser.parse(date) + timedelta(days=30)).strftime("%Y-%m-%d")
    error_msg = (f"""\nInvalid input error.
    - Make sure the date is in the format (YYYY-MM-DD)
    - Make sure the date is between the ({date}) and ({date_max})
    - Make sure all values are greater than zero""")
    
    return error_msg
    

def get_time(result_date, now_date):
    """This function gets the event time for the slot from the user, the time must be
    at least 30 minutes later than the current time."""
    
    input_time = input("    Enter time (HH:MM): ")

    match = re.match("\d\d:\d\d", input_time) is None

    if match != None:
        # Value error check
        time = parser.parse(now_date) + timedelta(hours=1)
        input_date = parser.parse(now_date.split(" ",1)[0] + " " + input_time)
        input_time = parser.parse(input_time)

        time_valid = input_time >= time
        date_valid = result_date.date() > time.date()
        date_valid2 = result_date.date() < (time + timedelta(days=7)).date()
        result = (time_valid or date_valid) and date_valid2
        time_min = dt.time(7,0,0)
        time_max = dt.time(16,30,0)
        valid = input_time.time() >= time_min and input_time.time() <= time_max

        if result and valid:
            return input_time

    error_msg = (f"""\nInvalid input error.
    - You must book an hour before session time
    - Specify a time between 07:00-17:00
    - Make sure the time is in the format (HH:MM:SS)""")

    return error_msg


def get_summary_and_description():
    """
    This function gets the event summary from the user.
    """

    summary = input("    Enter topic: ")
    if summary != "":
        description = input("    Enter description: ")
        if description != "":
            return summary, description

    return None, None


def get_params():
    """
    This function gets the parameters (datetime and summary) needed to create
    a slot and returns a tuple of them.
    """

    now = datetime.now()
    date = get_date(now.strftime("%Y-%m-%d"))

    if type(date) != dt.datetime:
        return None, None, None, None

    time = get_time(date, now.strftime("%Y-%m-%d %H:%M:%S"))
    if type(time) != dt.datetime:
        return None, None, None, None
    
    summary, description = get_summary_and_description()

    if type(summary) == None:
        print("Invalid input error.\n\tSummary cannot be empty")
        return None, None, None, None

    if type(description) == None:
        print("Invalid input error.\n\tDescription cannot be empty")
        return None, None, None, None
    
    start = date.strftime("%Y-%m-%d") + "T" + time.strftime("%H:%M:%S+02:00")

    end = parser.parse(start) + timedelta(minutes=30)
    end = end.strftime("%Y-%m-%dT%H:%M:%S+02:00")

    return start, end, summary, description


def create_event(start, end, summary, description, email):
    """This function creates an event (slot), in the calendar and returns the 
    event id."""

    service = get_service()

    conference_random_key = f'{random.randrange(1, 10**10)}'

    event_result = service.events().insert(calendarId='wtcteam19jhb@gmail.com', 
        conferenceDataVersion=1,
        body={
            "summary": summary,
            "description": description,
            "start": {
                "dateTime": start,
                "timeZone": "Africa/Johannesburg"
            },
            "end": {
                "dateTime": end,
                "timeZone": "Africa/Johannesburg"
            },
            "conferenceData": {
                "createRequest": {
                    "requestId": conference_random_key,
                    "conferenceSolutionKey": {
                        "type": "hangoutsMeet"
                    }
                }
            },
            "status": 'tentative',
            "creator": { "email": email }
        }).execute()

    time_start = event_result['start']['dateTime'][11:16]
    end_time = event_result['end']['dateTime'][11:16]

    msg = colored("Created [OPEN] volunteer slot", "cyan")
    print(f"\n\n{msg}\n")
    print("\tCreator:\t", email)
    print("\tSlot ID:\t", colored(event_result['id'], 'yellow'))
    print("\tSummary:\t", event_result['summary'])
    print("\tDescription:\t", event_result['description'])
    print("\tDate:\t\t", event_result['start']['dateTime'][:10])
    print("\tTime:\t\t", f'{time_start} - {end_time}')
    print("\n")

    return event_result['id']


