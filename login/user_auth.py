from os import path
from calendar_setup.calendar_service import *
from datetime import datetime, timedelta
from termcolor import colored
import sys
import os
import json
from bookings.processing_data import *
from bookings.list_calendars import get_code_clinics_calendar

# The token file location
token_path = f'{sys.path[0]}/creds/token.pickle'
config_path = f"{sys.path[0]}/files/json/.config.json"


def get_time_date():
    """Getting the current time and date. This function returns a dictionary
    of time and date."""

    now = datetime.now()
    date = now.strftime("%D")
    time = now.strftime("%H:%M")

    date_and_time = {
        "date": date,
        "time": time
    }

    return date_and_time


def get_user_details():
    """Retrieving user details from the calendar setup module."""

    events_results = get_events_results()
    
    user_email = events_results.get('summary')
    username = user_email.split('@')[0]
    date_and_time = get_time_date()

    user_details = {
        "username": username,
        "email": user_email,
        "date": date_and_time['date'],
        "time": date_and_time['time']
    }

    return user_details


def remove_token():
    """ Removing the token file if the user is not logged in or if the token
    file exists.""" 

    is_found = True

    try:
        os.remove(token_path)
    except FileNotFoundError:
        is_found = False
        print("You already loggged out!")
        print("\nPlease run: \"wtc-cal login\"\n")

    return is_found


def validate_email(user_email):
    """Ths function checks if used email is in the WeThinkCode_ organization.
    It should check if the domain contains '@student.wethinkcode.co.za' for 
    students or '@wethinkcode.co.za' for the staff."""

    user_name = user_email.split('@')[0]
    domain_name = user_email.split('@')[1]

    if domain_name.find("wethinkcode.co.za") > -1:
        msg = colored(f"Welcome {str(user_name).capitalize()}!", "green")
        print(msg)
    else:
        remove_token()
        print("Invalid email address!")


def writing_to_json_file():
    """Writing user data to a hidden .config file."""

    user_details = get_user_details()

    with open(config_path, 'w') as write_config:
        json.dump(user_details, write_config, indent=4)


def get_user_status():
    """Getting the status of the signed in user. If they're signed in, it should
    print out that the user is logged in, if not, then it should instructions to
    the user about loggin in."""

    if path.exists(token_path):
    
        user_email = get_user_email()   

        connected = colored('[CONNECTED]', 'green')
        print(connected + " Google Calendar | Code Clinic Booking System") 
        print(f"Signed in as {user_email}")
    else:
        offline = colored('[OFFLINE]', 'red')
        print(offline + "\nPlease run: \"wtc-cal login\"")


def user_login():
    """Signing the user by redirecting them to the sign in page. If they are
    logged in, print out a statemet. If they're not, create a token file for
    them."""        

    if not path.exists(token_path):
        writing_to_json_file()

        user_email = get_user_email()
        os.system('clear')
        validate_email(user_email)
    else:
        print("You are already logged in!")


def user_logout():
    """Loggin out the user from the booking sysem."""

    if remove_token():
        print(colored("You have successfully logged out!", "yellow"))


def get_login_state():
    """This function checks whether the user is logged in or not.
        > Returns a boolean."""

    if path.exists(token_path):
        return True
    else:
        return False


def show_config():
    """This function displays the config file."""

    config = None
    if os.path.exists(config_path):
        with open(config_path, 'r') as json_file:
            config = json.load(json_file)

        print(f"Reading config from {sys.path[0]}/.config.json\n")
        print("Config {")
        print(f"    editor: wtc-cal")
        print(f"    repo_path: \"{sys.path[0]}\"")
        print(f"    username: \"{config.get('email')}\"")
        print("    code_clinics_manager: \"wtcteam19jhb@gmail.co.za\"")
        print("}")
    else:
        print("Config file does not exist")


def get_user_email():
    """Getting the data from the json file"""

    user_details = None

    with open(config_path, 'r') as json_file:
        user_details = json.load(json_file)

    user_email = user_details.get('email')

    return user_email


def auto_logout():
    """
    This function checks if your token is still valid
    """
    
    if path.exists(token_path):
    
        data = None

        with open(config_path, 'r') as json_file:
            data = json.load(json_file)
    
        # Parse type string date and time objects to integer type objects
        hours = int(data['time'][:2])
        mins = int(data['time'][3:5])
        mon = int(data['date'][:2])
        day = int(data['date'][3:5])
        year = int('20'+data['date'][6:8])
        
        #logout_time = date + timedelta(hours=2)
        date = datetime(year=year, month=mon, day=day, hour=hours, minute=mins)    
        logout_time = date + timedelta(hours=2)
        
        if(datetime.now() > logout_time):
            save_data(get_code_clinics_calendar())
            remove_token()
            return True

    return False   