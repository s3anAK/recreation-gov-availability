import requests
from datetime import datetime

#api_key = input("Enter your api key")

permit_area= input("Please enter your desired area. Supported options include 'Inyo National Forest' and 'SEKI National Park' ")
permit_codes = {'Inyo National Forest': 233262, "SEKI National Park": 445857}
starting_date= input("Please enter your desired starting date in the format yyyy-mm-dd")
ending_date= input("Please enter your desired ending date in the format yyyy-mm-dd")


recreation_url = ("https://www.recreation.gov/api/permitinyo/" + str(permit_codes[permit_area]) + "/availability?start_date=2022-05-01&end_date=2022-05-31&commercial_acct=false")
print(recreation_url)