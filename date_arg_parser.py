import datetime
from dateutil import rrule
import calendar

class date_parser:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.months = ''

    def start_of_month(self):
        self.start_date = datetime.date(int(self.start_date[0:4]), int(self.start_date[5:6]), 1)
        print(self.start_date)
        self.end_date = datetime.date(int(self.end_date[0:4]), int(self.end_date[5:6]), int(self.end_date[8:9]))
        print(self.end_date)
        self.months = list(rrule.rrule(rrule.MONTHLY, dtstart=self.start_date, until=self.end_date))
        print(self.months)


    def month_and_date_parser(self):
        if int(self.start_date[5]) == 0:
            self.start_date= self.start_date[:5] + self.start_date[6:]
        if int(self.end_date[5]) == 0:
            self.end_date= self.end_date[:5] + self.end_date[6:]
        if int(self.start_date[8]) == 0:
            self.start_date = self.start_date[:8] + self.start_date[9:]
        if int(self.end_date[8]) == 0:
            self.end_date = self.end_date[:8] + self.end_date[9:]

    def date_formatter(self):
        counter = 0
        for i in self.months:
            self.months[counter] = datetime.date(i.year,i.month,i.day)
            counter += 1

'''
    def end_dates(self):
        print(self.months)
        counter = 0
        for i in self.months:
            print(i)
            self.months.insert(counter+1, datetime(i.year, i.month, calendar._monthlen(i.year, i.month)))
            counter += 1
            print(self.months)
'''





