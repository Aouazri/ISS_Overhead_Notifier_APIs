import requests
import datetime as dt
import smtplib
import time

MY_LAT = 33.248348
MY_LONG = -8.516350
# ISS Data
response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()

data = response.json()

iss_longitude = float(data["iss_position"]["longitude"])
iss_latitude = float(data["iss_position"]["latitude"])

# Getting the Sunrise and Sunset time for my location

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0
}

response = requests.get(url="http://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()['results']
sunrise = data["sunrise"]
sunset = data["sunset"]
# sunrise hour
sunrise_list = sunrise.split("T")
sunrise_hour = int(sunrise_list[1].split(':')[0])
# sunset hour
sunset_list = sunset.split("T")
sunset_hour = int(sunset_list[1].split(':')[0])

# current time
time_now = dt.datetime.now()
current_hour = int(time_now.hour)


def iss_in_proximity():
    """a function that checks if the ISS is nearby within a distance of -+5 degrees"""
    close_proximity = False
    my_position = (MY_LAT, MY_LONG)
    iss_position = (iss_latitude, iss_longitude)
    lat_dif = abs(iss_position[0] - my_position[0])
    lgt_dif = abs(iss_position[1] - my_position[1])
    if (lat_dif <= 5) and (lgt_dif <= 5):
        close_proximity = True
    return close_proximity


def night_time():
    """a function that returns True if it's nighttime and False Otherwise"""
    if current_hour >= sunset_hour or current_hour <= sunrise_hour:
        return True
    else:
        return False


my_email = "yourmail@gmail.com"
password = "yourPassword"


def send_mail():
    if night_time() and iss_in_proximity():
        print("it's nighttime and the iss is close")
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=my_email,
                msg="Subject: ISS is NEARBY!\n\n Look at the sky"
            )


# check every 60 seconds
while True:
    time.sleep(60)
    send_mail()
