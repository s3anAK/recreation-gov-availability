import requests
import datetime
from date_arg_parser import date_parser
import calendar

#api_key = input("Enter your api key")

permit_area= input("Please enter your desired area. Supported options include 'Inyo National Forest' and 'SEKI National Park' ")
permit_codes = {'Inyo National Forest': 233262, "SEKI National Park": 445857}
starting_date_input= input("Please enter your desired starting date in the format yyyy-mm-dd")
ending_date_input= input("Please enter your desired ending date in the format yyyy-mm-dd")
url_list =[]

date=date_parser(starting_date_input,ending_date_input)
date.month_and_date_parser()
date.start_of_month()
date.date_formatter()

for i in date.months:
    ending_date = datetime.date(i.year,i.month,calendar._monthlen(i.year,i.month))
    temp_url = ("https://www.recreation.gov/api/permitinyo/" + str(permit_codes[permit_area]) + "/availability?start_date=" + str(i) + "&end_date=" + str(ending_date) + "&commercial_acct=false")
    url_list.append(temp_url)
    #print(temp_url)

print(url_list)

#recreation_url = ("https://www.recreation.gov/api/permitinyo/" + str(permit_codes[permit_area]) + "/availability?start_date=2022-05-01&end_date=2022-05-31&commercial_acct=false")
#print(recreation_url)