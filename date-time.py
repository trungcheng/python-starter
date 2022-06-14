from datetime import date
from datetime import datetime

today = date.today()
my_date = date(1996, 12, 11)

print("Today's date is", today)
print("Current year:", today.year)
print("Current month:", today.month)
print("Current day:", today.day)
print("Date passed as argument is", my_date)

# Getting Datetime from timestamp
date_time = datetime.fromtimestamp(1887639468)
print("Datetime from timestamp:", date_time)

# Converting the date to the string
Str = date.isoformat(today)
print("String Representation", Str)
print(type(Str))
