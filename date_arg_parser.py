import datetime
from dateutil import rrule
import re

class date_parser:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.months = ''
        self.dates = ''

    def month_and_date_parser(self):
        self.dates=[self.start_date.split('-'),self.end_date.split('-')]
        count1 = 0
        count2 = 0
        for date in self.dates:
            for part in date:
                part = re.sub('^0','',part)
                self.dates[count1][count2] = part
                count2 += 1
            count1 += 1
            count2=0

    def start_of_month(self):
        self.start_date = datetime.date(int(self.dates[0][0]), int(self.dates[0][1]), 1)
        #print(self.start_date)
        self.end_date = datetime.date(int(self.dates[1][0]), int(self.dates[1][1]), int(self.dates[1][2]))
        #print(self.end_date)
        self.months = list(rrule.rrule(rrule.MONTHLY, dtstart=self.start_date, until=self.end_date))
        #print(self.months)

    def date_formatter(self):
        counter = 0
        for i in self.months:
            self.months[counter] = datetime.date(i.year,i.month,i.day)
            counter += 1





