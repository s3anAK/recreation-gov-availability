import requests
import datetime
import calendar
import json
from fake_useragent import UserAgent
from dateutil import rrule
import re
import smtplib
from email.message import EmailMessage
import argparse
from secrets import *


def date_maker(date, start_of_month=False):
    date = date.split('-')
    counter = 0
    for i in date:
        i = re.sub('^0', '', i)
        date[counter] = i
        counter += 1
    if start_of_month == True:
        date = datetime.date(int(date[0]), int(date[1]), 1)
    else:
        date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
    return date

def format_months(months):
    counter = 0
    for i in months:
        months[counter] = datetime.date(i.year, i.month, i.day)
        counter += 1

def get_permit_entrance_id():
    entrance_url = 'https://ridb.recreation.gov/api/v1/facilities/233262/permitentrances'
    payload = {'query': permit_entrance}
    headers = {'apikey': API_KEY}
    results = requests.get(entrance_url, headers=headers, params=payload)
    results = json.loads(results.text)
    permit_entrance_id = (results['RECDATA'][0]['PermitEntranceID'])
    return permit_entrance_id

def get_availability():
    ua = UserAgent()
    availability_list_unformatted = []
    for i in url_list:
        availability_url = i
        headers = {'apikey': API_KEY, "user-agent": ua.random}
        availability = requests.get(availability_url, headers=headers)
        availability = json.loads(availability.text)
        availability_list_unformatted.append(availability)
    return availability_list_unformatted

def check_availability(availability_list, permit_entrance_id, start_date, end_date,group):
    count = 0
    availability_dict_formatted = {}
    for month in availability_list:
        for key1, value1 in month.items():
            for key2, value2 in value1.items():
                temp_date = date_maker((key2))
                if start_date <= temp_date <= end_date:
                    for key3, value3 in value2.items():
                        if key3 == permit_entrance_id:
                            if month[key1][key2][key3]['remaining'] >= group and month[key1][key2][key3]['remaining'] < 100:
                                availability_dict_formatted[key2] = month[key1][key2][key3]['remaining']
                                count += 1
                            if month[key1][key2][key3]['remaining'] > 105:
                                print(
                                    'This is a non quota permit. Reservations will sometimes release a week before, but there will always be an unlimited amount.')
                                quit()
    if count == 0:
        print("sorry this permit is not available in your selected range")

    return availability_dict_formatted

def send_email(availability_dict_formatted):
    body = "This is an automated message from Sean's Inyo National Forest permit checker. Permits that you have requested from recreation.gov have become available." + '\n'
    body = body + '\n' + "Here is the informaton you entered for this trip:"
    body = body + '\n' + "Starting Date: " + starting_date_input
    body = body + '\n' + "Ending Date: " + ending_date_input
    body = body + '\n' + "Permit Entrance Code: " + permit_entrance
    body = body + '\n' + "Group Size: " + str(group_size)
    body = body + '\n' + "API Key (for use with recreation.gov): " + API_KEY
    body = body + '\n' + "Receiving Email Address: " + receiving_address + '\n' + '\n'

    for date, available in availability_dict_formatted.items():
        if available > 1:
            body = body + 'There are ' + str(available) + ' permits available on ' + date
        else:
            body = body + 'There is ' + str(available) + ' permit available on ' + date
        body = body + '\n'

    body = body + '\n' + 'You can reserve your permit here (note that you will have to enter your information again):'
    body = body + '\n' + 'https://www.recreation.gov/permits/233262/registration/detailed-availability?date=2022-07-29&type=overnight-permit'

    #print(body)
    msg = EmailMessage()
    msg['Subject'] = 'Your permit for ' + permit_entrance + ' is available!'
    msg['From'] = 'seankingus@gmail.com'
    msg['To'] = receiving_address
    msg.set_content(body)

    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:

        smtp.login('seankingus@gmail.com','drxyqcindfhfmhgd')

        smtp.send_message(msg)

parser = argparse.ArgumentParser(description='finds permit availability for Inyo National Forest')
parser.add_argument('start_date', type=str, help='your desired starting date in the format yyyy-mm-dd')
parser.add_argument('end_date', type=str, help='your desired ending date in the format yyyy-mm-dd')
parser.add_argument('permit_entrance_id', type=str, help='enter your permit entrance id from recreation.gov')
parser.add_argument('receiving_address', type=str, help='enter the email you wish to receive updates from')
parser.add_argument('group_size', type=str, help='enter your group size (max of 15)')

args = parser.parse_args()

permit_entrance = args.permit_entrance_id
starting_date_input = args.start_date
ending_date_input = args.end_date
receiving_address = args.receiving_address
group_size = int(args.group_size)
url_list = []


if permit_entrance == 'HH01':
    permit_entrance = "HH11"

start_date = date_maker(starting_date_input)
start_of_month = date_maker(starting_date_input, True)
end_date = date_maker(ending_date_input)
months = list(rrule.rrule(rrule.MONTHLY, dtstart=start_of_month, until=end_date))
format_months(months)

for i in months:
    end_of_month = datetime.date(i.year, i.month, calendar._monthlen(i.year, i.month))
    temp_url = ("https://www.recreation.gov/api/permitinyo/233262/availability?start_date=" + str(
        i) + "&end_date=" + str(end_of_month) + "&commercial_acct=false")
    url_list.append(temp_url)

permit_entrance_id = get_permit_entrance_id()
availability_list_unformatted = get_availability()
availability_dict_formatted = check_availability(availability_list_unformatted, permit_entrance_id, start_date, end_date,group_size)
send_email(availability_dict_formatted)
