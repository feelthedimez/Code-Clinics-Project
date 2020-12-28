# Code Clinics Group Project

Code Clinics is a booking CLI system that uses Google API. A patient needs to book a specific time slot to attend a Coding Clinic session, and typically these sessions are one-on-one sessions with a more experienced person who can advise on the coding problem at hand. It only works with `@wethinkcode.co.za` email domain only as default.

# Installation 
## Requirements
This system works on a Linux/iMac with bash terminal.

## Cloning the repo

Please add the git repo to your home directory. Run all the steps in order as they appear in this document:

```bash
cd ~/
git clone https://github.com/DamianOdendaal/code-clinic-booking-system.git
```

## Setup the System

Make sure you are in ```codeclinics``` directory, then run:

```bash
cd code-clinic-booking-system/codeclinics
chmod +x cal-setup
chmod +x wtc-cal
```

## Bash Configuration

Run the script below in your bash terminal:

```bash
code ~/.bashrc
```

Then inside that ```.bashrc``` file, add the script below at the end of the ```.bashrc``` file.

```bash
export PATH="$HOME/code-clinic-booking-system/codeclinics:$PATH"
```

## Installing Dependencies

Run the following command from any directory to download required packages:

```bash
cal-setup
```

## Running the System

Run the following to see what type of CLI commands work with our system.

### Code Clinic Commands

```bash
wtc-cal
````
## Working with your Personal Calendar

If you're not in @wethinkcode.co.za email organization, the system will automatically kick you out. So, to move around that, go to:

```bash
code ~/code-clinic-booking-system/codeclinics/login/user_auth.py
```
On the function ```def validate_email()``` on line 67, change the statement of the email ```@wethinkcode``` to your prefered email domain of your organisation - it can event be ```@gmail.com``` for testing purposes. 


### Bonus Functionality

There is an ics file - which is a Calendar Document. You can open it and see the bookings in an Application of your choice.

Path: 
```bash
~/code-clinic-booking-system/codeclinics/files/ics
```

### Volunteering for a slot

```bash
wtc-cal volunteer
````

### Viewing Slots

```bash
wtc-cal slots
````

### Booking a Slot

```bash
wtc-cal book <ui_code>
```

### Cancelling a Slot or Cancelling a Booking

```bash
wtc-cal cancel <ui_code>
```

### Things still to be Done

1. Adding more tests for certain modules.
2. Adding a functionality that will make the volunteer and patient 'status' to the event respond to 'Going' instead of 'Maybe'.
3. Making the terminal scroll horizontally rather than text wrapping information - and making the terminal output be clustered.

# Authors and Acknowledgement

## Team Members who made this System Possible

Thabang Soulo,
Nkosingiphile Nkosi,
Nicholas Brummer,
Princess Lamola,
Kamogelo Mohlabu, and
Tebogo Tema

Also, all thanks to WeThinkCode for making us think outside the box. We really learned a lot just from working on this simple system.
