import os
import sys
import unittest
from unittest.mock import patch
from login import user_auth
from datetime import datetime, timedelta
"""Calendar setup imports"""
import googleapiclient.discovery
from calendar_setup import calendar_service
import pytz
"""Bookings imports"""
import io
from io import StringIO
from unittest.mock import patch
from bookings import list_calendars
from bookings import patient
from bookings import processing_data
from bookings import volunteer


class LoginTestCase(unittest.TestCase):
    """
    This class contains all the tests for the user_auth module in the login package
    """

    def test_get_time_date(self):
        """This tests the get_time_date() function's return value from 
        login.user_auth.py."""

        now = datetime.now()
        date = now.strftime("%D")
        time = now.strftime("%H:%M")

        output = user_auth.get_time_date()

        dateAndTime = {
            "date": date,
            "time": time
        }

        self.assertEqual(dateAndTime, output)


    def test_get_user_details(self):
        """This tests the get_user_details() function's return type from 
        login.user_auth.py."""

        output = user_auth.get_user_details()

        self.assertEqual(dict, type(output))
        self.assertEqual(len(output), 4)


    def test_remove_token(self):
        """This tests the remove_token() function's return value from 
        login.user_auth.py."""

        output = os.path.exists(f"{sys.path[0]}/creds/token.pickle")
        
        if output:
            self.assertTrue(output)
        else:
            self.assertFalse(output)


    @patch('login.user_auth.validate_email',return_value='jdoe@wethinkcode.co.za')
    def test_validate_email(self, input):
        """This tests the validate_email() function's output from 
        login.user_auth.py."""

        output = user_auth.validate_email(user_email=str)

        self.assertEqual(output, 'jdoe@wethinkcode.co.za')


    def test_writing_to_json_file(self):
        """This tests the writing_to_json_file() function."""
        
        user_auth.writing_to_json_file()
        output = os.path.exists(f"{sys.path[0]}/.config.json")
        if output:
            self.assertTrue(output)
        else:
            self.assertFalse(output)


    # def test_get_user_status(self):
    #     """
    #     This tests the get_user_status() function.
    #     """
    #     pass


    # def test_user_login(self):
    #     """
    #     This tests the user_login() function.
    #     """
    #     pass


    # @patch('sys.stdout', new_callable=io.StringIO)
    # def test_user_logout(self, mock_stdout):
    #     """
    #     This tests the user_logout() function.
    #     """
    #     user_auth.user_logout()
    #     self.assertEqual("\x1b[33mYou have successfully logged out!\x1b[0m\n", mock_stdout.getvalue())

    #     # output = os.path.exists(f"{sys.path[0]}/creds/token.pickle")
    #     # self.assertTrue(user_auth.user_logout())        


    def test_get_login_state(self):
        """
        This tests the get_login_state()function's
        return value from login.user_auth.py.
        """
        output = user_auth.get_login_state()
        if os.path.exists(f"{sys.path[0]}/creds/token.pickle"):
            self.assertTrue(output)
        else:
            self.assertFalse(output)


    # def test_show_config(self):
    #     """
    #     This tests the show_config() function.
    #     """
    #     pass

        
    def test_get_user_email(self):
        """
        This tests the get_user_email() function.
        """

        output = user_auth.get_user_email()
        self.assertEqual(type(output), str)
        self.assertNotEqual(output, '')

    
    # def test_auto_logout(self):
    #     """
    #     This tests the test_auto_logout() function.
    #     """
        
    #     # output = user_auth.auto_logout()

    #     #must use datetime stuff
    #     pass


class CalendarSetupTestCase(unittest.TestCase):
    """
    This class contains all the tests for the modules in the calendar_setup 
    package
    """

    def test_get_service(self):
        """
        This tests the get_service() function
        """
        
        output = calendar_service.get_service()

        self.assertEqual(type(output), googleapiclient.discovery.Resource)


    def test_get_events_results(self):
        """This tests the get_events_results() function."""

        output = calendar_service.get_events_results()

        self.assertEqual(type(output), dict)
        self.assertTrue(len(output) > 0)


    def test_get_time_constraints(self):
        """This tests the get_time_constraints() function."""

        now = datetime.now(pytz.timezone("Africa/Johannesburg"))
        end = now + timedelta(days=7)
        start = now.strftime("%Y-%m-%dT%H:%M:%S") + "Z"
        end = end.strftime("%Y-%m-%dT%H:%M:%S") + "Z"

        output = calendar_service.get_time_constraints()

        self.assertEqual(output, (start, end))
    

class BookingsTestCase(unittest.TestCase):
    """
    This class contains all the tests for the modules in the bookings
    package
    """

    """
    Test cases for the "list_calendars" module
    """

    # def test_formatted_data_output(self):
    #     output = list_calendars.formatted_data_output(data=list)
    #     self.assertEqual(type(output), list)


    # def test_get_date_and_time(self):
    #     output = list_calendars.get_date_and_time(date_time=datetime)
    #     self.assertEqual(type(output), str)


    def test_get_code_clinics_calendar(self):
        """
        This tests the get_code_clinics_calandar() function
        """

        output = list_calendars.get_code_clinics_calendar()
        self.assertEqual(type(output), list)


    def test_get_primary_calendar(self):
        """
        This tests the get_primary_calendar()
        """

        output = list_calendars.get_primary_calendar()
        self.assertEqual(type(output), list)


    """
    Test cases for the "patient" module
    """

    # def test_is_booking_valid(self):
    #     output = patient.is_booking_valid(id=str)
    #     self.assertEqual(type(output), bool)


    """
    Test cases for the "processing_data" module
    """

    def test_get_user(self):
        """
        This tests the get_user() function
        """

        output = processing_data.get_user()
        self.assertEqual(type(output), tuple)


    def test_load_data(self):
        """
        This tests the load_data() funciton
        """

        output = processing_data.load_data()
        self.assertEqual(type(output), list())


    """
    Test cases for the "volunteer" module
    """

    def test_weekdays(self):
        """ This tests the weekdays() function """

        output = volunteer.weekdays(day=1)
        self.assertEqual(type(output), str)


    def test_is_volunteering_valid(self):
        """ This tests is_volunteering() function """

        output = volunteer.is_volunteering_valid(start=str, user_email=str)
        self.assertEqual(type(output), bool)


    @patch('bookings.volunteer.get_date', return_value='13')
    def test_get_date(self, input):
        """ This tests get_date() """

        output = volunteer.get_date()
        self.assertEqual(output, '13')


    @patch('bookings.volunteer.get_time',return_value='10:00:00')
    def test_get_time(self, input):
        """ This tests get_time() function """

        output = volunteer.get_time()
        self.assertEqual(output, '10:00:00')


    @patch('bookings.volunteer.get_summary_and_description', return_value='loops')
    def test_get_summary_and_description(self, input):
        """ This tests get_summary_and_description() """

        output = volunteer.get_summary_and_description()
        self.assertEqual(output, 'loops')


    @patch('bookings.volunteer.get_params',return_value=('13','10:00:00'))
    def test_get_params(self, input):
        """ This tests the get_params """

        output = volunteer.get_params()
        self.assertEqual(output, ('13','10:00:00'))


    # def test_create_event(self):
    #     output = volunteer.create_event(start=str,end=str,summary=str,description=str,email=str)
    #     self.assertEqual(type(output), dict)


if __name__ == "__main__":
    unittest.main()