import requests
import datetime
from date_arg_parser import date_parser
import calendar
import json

api_key = 'ab3f1f1a-9cc2-4c20-bff6-dbf3a2d9fa96'

#permit_area= input("Please enter your desired area. Supported options include 'Inyo National Forest' and 'SEKI National Park' ")
permit_area = "Inyo National Forest"
permit_codes = {'Inyo National Forest': 233262, "SEKI National Park": 445857}
#starting_date_input= input("Please enter your desired starting date in the format yyyy-mm-dd ")
starting_date_input='2022-08-03'
#ending_date_input= input("Please enter your desired ending date in the format yyyy-mm-dd ")
ending_date_input="2022-08-21"
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

test_entrance = 'Baxter Pass'
entrance_url = 'https://ridb.recreation.gov/api/v1/facilities/' + str(permit_codes[permit_area]) + '/permitentrances'
payload = {'query': test_entrance}
headers = {'apikey': api_key}
results = requests.get(entrance_url,headers=headers, params=payload)
results = json.loads(results.text)
permit_entrance_id = (results['RECDATA'][0]['PermitEntranceID'])
print(permit_entrance_id)


