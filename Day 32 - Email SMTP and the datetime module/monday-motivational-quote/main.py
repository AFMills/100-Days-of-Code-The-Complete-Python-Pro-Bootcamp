# # App Password: pmac sgaj ylvx xtbn
#
# import smtplib
#
# my_email = "tafkaa0@gmail.com"
# password = "pmacsgajylvxxtbn"
#
# with smtplib.SMTP("smtp.gmail.com", 587) as connection:
#         connection.starttls()       # Secures email by encrypting it
#         connection.login(user=my_email, password=password)
#         connection.sendmail(from_addr=my_email,
#                             to_addrs="tafkaa0@yahoo.com",
#                             msg="Subject:Hello\n\nThis is the body of my email."
#         )


# import datetime as dt
#
# now = dt.datetime.now()
# year = now.year
# month = now.month
# day = now.day
# hour = now.hour
# minute = now.minute
# day_of_week = now.weekday()         #Returns day of the week as an integer, starting from Monday as 0
# print(day_of_week)
#
# date_of_birth = dt.datetime(year=1998, month=1, day=1, hour=4)
# print(date_of_birth)

import smtplib
import datetime as dt
import random

MY_EMAIL = "tafkaa0@gmail.com"
MY_PASSWORD = "pmacsgajylvxxtbn"

now = dt.datetime.now()
weekday = now.weekday()
if weekday == 0:
    with open("quotes.txt") as quote_file:
        all_quotes = quote_file.readlines()
        quote = random.choice(all_quotes)
    print(quote)

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=MY_EMAIL,
                            msg=f"Subject: Monday Motivation\n\n{quote}")