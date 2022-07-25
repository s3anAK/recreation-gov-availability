import requests
import datetime
from date_arg_parser import date_parser
import calendar
import json
from fake_useragent import UserAgent

api_key = 'ab3f1f1a-9cc2-4c20-bff6-dbf3a2d9fa96'

#permit_area= input("Please enter your desired area. Supported options include 'Inyo National Forest' and 'SEKI National Park' ")
permit_area = "Inyo National Forest"
permit_codes = {'Inyo National Forest': 233262, "SEKI National Park": 445857}
#starting_date_input= input("Please enter your desired starting date in the format yyyy-mm-dd ")
starting_date_input='2022-08-03'
#ending_date_input= input("Please enter your desired ending date in the format yyyy-mm-dd ")
ending_date_input="2023-01-21"
permit_entrance=input("Please enter the ID for your desired trailhead ")
if permit_entrance == 'HH01':
    permit_entrance = "HH11"
url_list =[]

date=date_parser(starting_date_input,ending_date_input)
date.month_and_date_parser()
date.start_of_month()
date.date_formatter()

for i in date.months:
    ending_date = datetime.date(i.year,i.month,calendar._monthlen(i.year,i.month))
    temp_url = ("https://www.recreation.gov/api/permitinyo/" + str(permit_codes[permit_area]) + "/availability?start_date=" + str(i) + "&end_date=" + str(ending_date) + "&commercial_acct=false")
    url_list.append(temp_url)

print(url_list)

def get_permit_entrance_id():
    #test_entrance = 'Glacier Canyon'
    entrance_url = 'https://ridb.recreation.gov/api/v1/facilities/' + str(permit_codes[permit_area]) + '/permitentrances'
    payload = {'query': permit_entrance}
    headers = {'apikey': api_key}
    results = requests.get(entrance_url,headers=headers, params=payload)
    results = json.loads(results.text)
    permit_entrance_id = (results['RECDATA'][0]['PermitEntranceID'])
    return permit_entrance_id
    #print(permit_entrance_id)

def get_availability():
    ua = UserAgent()
    availability_list = []
    for i in url_list:
        availability_url = i
        headers = {'apikey': api_key, "user-agent": ua.random}
        availability = requests.get(availability_url,headers=headers)
        #print(availability)
        availability = json.loads(availability.text)
        availability_list.append(availability)
        print(len(availability_list))
    return availability_list

def check_availability(availability_list,permit_entrance_id):
    for month in availability_list:
        for key1,value1 in month.items():
            for key2,value2 in value1.items():
                for key3, value3 in value2.items():
                    if key3==permit_entrance_id:
                        if month[key1][key2][key3]['remaining'] > 0 and month[key1][key2][key3]['remaining'] < 100:
                            print('this permit is available on', key2)
                        if month[key1][key2][key3]['remaining'] > 105:
                            print('This is a non quota permit. Reservations will sometimes release a week before, but there will always be an unlimited amount.')
                            quit()


permit_entrance_id = get_permit_entrance_id()
availability_list = get_availability()
check_availability(availability_list, permit_entrance_id)

