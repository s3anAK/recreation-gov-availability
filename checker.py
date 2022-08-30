import requests
import datetime
import calendar
import json
from fake_useragent import UserAgent
from dateutil import rrule
import re
import smtplib
from email.message import EmailMessage
from secrets import *
import logging

def date_maker(date, start_of_month=False):
    """
    This function takes a date in the format yyyy-mm-dd and converts it to a datetime object for use with date calculations.
    :param date: The date in the format yyyy-mm-dd that you wish to convert to a datetime object
    :param start_of_month: A boolean paramater for if you want to convert the date to the first of the month
    :return: A datetime object
    """
    date = date.split('-')
    counter = 0
    for i in date:
        # removes the leading 0 from the element of the date, if there is one
        i = re.sub('^0', '', i)
        # redefines the element of the date without the leading 0
        date[counter] = i
        counter += 1
    # if the user has specified, the first of the month is automatically used. Otherwise, the date is kept the same.
    if start_of_month == True:
        date = datetime.date(int(date[0]), int(date[1]), 1)
    else:
        date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
    return date


def send_email(availability_dict_formatted):
    """
    This function generates an email to be sent to the user when their permit is availability.
    :param availability_dict_formatted: A dictionary of the dates for which a certain permit is available for a certain group size
    """
    # These statements build the message that will then be sent out as the body of the email
    body = "This is an automated message from Sean's Inyo National Forest permit checker. Permits that you have requested from recreation.gov have become available." + '\n'
    body = body + '\n' + "Here is the informaton you entered for this trip:"
    body = body + '\n' + "Desired Trailhead: " + name
    body = body + '\n' + "Starting Date: " + starting_date_input
    body = body + '\n' + "Ending Date: " + ending_date_input
    body = body + '\n' + "Permit Entrance Code: " + permit_entrance
    body = body + '\n' + "Group Size: " + str(group_size)
    body = body + '\n' + "API Key (for use with recreation.gov): " + API_KEY
    body = body + '\n' + "Receiving Email Address: " + receiving_address + '\n' + '\n'

    # Try to see if availability_dict_formatted is a dictionary or just a string
    try:
        availability_dict_formatted.items()
    except:

        # If it is a string, the body of the document simply becomes the error message about non-quota permits
        body = availability_dict_formatted
        subject = 'Your requested permit, ' + name + ', is a non-quota entrance'
    else:

        # If it is a dictionary, format the email to appropriately list all the available dates and how to reserve them
        for date, available in availability_dict_formatted.items():
            if available > 1:
                body = body + 'There are ' + str(available) + ' permits available on ' + date
            else:
                body = body + 'There is ' + str(available) + ' permit available on ' + date
            body = body + '\n'

        body = body + '\n' + 'You can reserve your permit here (note that you will have to enter your information again):'
        body = body + '\n' + 'https://www.recreation.gov/permits/233262/registration/detailed-availability?date=2022-07-29&type=overnight-permit'
        subject = 'Your permit for ' + name + ' is available!'
    finally:

        # In both cases (string or dictionary), this code actually sends the email using whatever subject and body were defined above
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = 'seankingus@gmail.com'
        msg['To'] = receiving_address
        msg.set_content(body)

        #Log into the mail server and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

            smtp.login('seankingus@gmail.com', 'drxyqcindfhfmhgd')

            smtp.send_message(msg)


def inyo_permits(starting_date_input, ending_date_input, permit_entrance, receiving_address, group_size, bool=False):
    """
    This function scrapes recreation.gov to see if permits are available for a desired trailhead, date, and group size.
    :param starting_date_input: A string in the form of yyyy-mm-dd containing the starting entry date
    :param ending_date_input: A string in the form of yyyy-mm-dd containing the ending entry date
    :param permit_entrance: The ID for the desired entry trailhead
    :param group_size: The group size for the permit
    :param bool: A boolean that dictates whether or not to send an email
    :return: True/False depending on whether or not to send an email along with either a dictionary of available dates or a message if the permit is special
    """

    # Turn the date strings into date objects for use with rrule
    start_date = date_maker(starting_date_input)
    start_of_month = date_maker(starting_date_input, True)
    end_date = date_maker(ending_date_input)

    # Create a list of months based on the start and end date
    months = list(rrule.rrule(rrule.MONTHLY, dtstart=start_of_month, until=end_date))

    # Create a list of URLs to query
    # Since the query dates must be the first and last of each month, the start_of_month variable is used rather than start_date
    url_list = []
    for i in months:
        start_of_month = datetime.date(i.year, i.month, i.day)
        end_of_month = datetime.date(i.year, i.month, calendar._monthlen(i.year, i.month))
        temp_url = ("https://www.recreation.gov/api/permitinyo/233262/availability?start_date=" + str(start_of_month) + "&end_date=" + str(end_of_month) + "&commercial_acct=false")
        url_list.append(temp_url)

    # Using the public permit ID that the user inputted, find the 3-digit ID that is not publicly available
    ua = UserAgent()
    entrance_url = 'https://ridb.recreation.gov/api/v1/facilities/233262/permitentrances'
    payload = {'query': permit_entrance}
    headers = {'apikey': API_KEY, "user-agent": ua.random}
    results = requests.get(entrance_url, headers=headers, params=payload)
    results = json.loads(results.text)
    permit_entrance_id = (results['RECDATA'][0]['PermitEntranceID'])

    # Using the list of URLs generated earlier, find the raw data about availability of all permits during those months
    ua = UserAgent()
    availability_list_unformatted = []
    for i in url_list:
        availability_url = i
        headers = {'apikey': API_KEY, "user-agent": ua.random}
        availability = requests.get(availability_url, headers=headers)
        availability = json.loads(availability.text)
        availability_list_unformatted.append(availability)

    # Search through the unformatted data to see if there are available permits and if so, add them to a formatted dictionary
    count = 0
    availability_dict_formatted = {}
    for month in availability_list_unformatted:
        for key1, value1 in month.items():
            for key2, value2 in value1.items():
                temp_date = date_maker((key2))
                if start_date <= temp_date <= end_date:
                    for key3, value3 in value2.items():
                        if key3 == permit_entrance_id:
                            if group_size <= month[key1][key2][key3]['remaining'] < 100:
                                availability_dict_formatted[key2] = month[key1][key2][key3]['remaining']
                                count += 1
                            # If there are more than 105 permits available, this means that the permit is a non-quota permit
                            if month[key1][key2][key3]['remaining'] > 105:
                                return True, 'This is a non quota permit. Reservations will sometimes release a week before, but there will always be an unlimited amount.'

    # If there are no permits available for the dates selected, check the availability of permits for current day in case the permits have not been released yet
    # If those are still no permits available, return nothing
    if count == 0:
        if bool == True:
            if 'This' in inyo_permits(str(datetime.date.today()), ending_date_input, permit_entrance, receiving_address, group_size)[1]:
                return True, 'This is a non quota permit. Reservations will sometimes release a week before, but there will always be an unlimited amount.'
            else:
                return False, ""
        else:
            pass

    return True, availability_dict_formatted

# Setup logging
logging.basicConfig(filename='logs.txt', level=logging.INFO, format='%(asctime)s %(message)s')

# Open and load the data from the trips file
f = open('trips.json')
data = json.load(f)

# Iterate through each trip and see if permits are available
for i in data['trailheads']:
    name = i['name']
    permit_entrance = i['ID']
    # This is to correct a blatant error by recreation.gov
    if permit_entrance == 'HH01':
        permit_entrance = "HH11"
    for trip in i['trips']:
        # Only execute this code if there are actually trips listed for a given trailhead
        if len(trip) > 0:
            starting_date_input = trip['starting_entry_date']
            ending_date_input = trip['ending_entry_date']
            group_size = trip['group_size']
            receiving_address = trip['email']
            checker = inyo_permits(starting_date_input, ending_date_input, permit_entrance, receiving_address, group_size, True)
            # If the returned boolean is True, then send an email
            if checker[0]:
                send_email(checker[1])
                logging.info('A successful call for ' + name + ' beginning on ' + starting_date_input + ' and ending on ' + ending_date_input + ' was executed.')
            # If the returned boolean is False, then do not send an email
            else:
                logging.info('An unsuccessful call for ' + name + ' beginning on ' + starting_date_input + ' and ending on ' + ending_date_input + ' was executed.')
