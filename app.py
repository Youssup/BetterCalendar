import config
import requests
import pytz

from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event
from gcsa.reminders import EmailReminder, PopupReminder
from beautiful_date import *
from datetime import datetime

# Get the user's location
def getUserLocation():
    params = {'key': config.key}
    response = requests.post('https://www.googleapis.com/geolocation/v1/geolocate', params=params)
    json = response.json()
    if 'location' in json:
        coordinates = json['location']
        params = {
            'latlng': f"{coordinates['lat']},{coordinates['lng']}",
            'key': config.key
        }
        response = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=params)
        json = response.json()
        if 'results' in json and len(json['results']) > 0:
            return json['results'][0]['formatted_address']
        else:
            print("Error: Something went wrong. Could not get user address.")
            return "None"
    else:
        print("Error: Something went wrong. Could not get location in json.")
        return "None"

# Get the longitude and latitude values of the address
def getLocation(address):
    params = {
        'address': address,
        'key': config.key
    }
    response = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=params)
    json = response.json()
    if 'results' in json and len(json['results']) > 0:
        return json['results'][0]['geometry']['location']
    else:
        print("Error: Something went wrong. Could not get location from address.")
        return "None"

# Get the travel time from the user's location to the event location
def get_directions(origin, destination):
    params = {
        'origin': origin,
        'destination': destination,
        'key': config.key
    }
    response = requests.get('https://maps.googleapis.com/maps/api/directions/json', params=params)
    json = response.json()
    if 'routes' in json and len(json['routes']) > 0:
        seconds = json['routes'][0]['legs'][0]['duration']['value']
        return round(seconds / 60)
    else:
        if "missing the 'destination' parameter." in json:
            print("Error: Missing destination parameter.")
        print("Error: Something went wrong. Could not get travel time.")
        return 0

# Add reminder to event 
def addReminder(event, reminder):
    event.reminders = [EmailReminder(minutes_before_start=reminder), PopupReminder(minutes_before_start=reminder)]
    gc.update_event(event)

# Parse event's description to find user variation
def setVariation(event):
    keyword = "!Extra Time: "
    description = event.description
    if(description == None or keyword not in description):
        return 0
    else:
        variation = description.split(keyword,1)[1].split('!',1)[0].strip()
        return int(variation)

# Sets the user's location
def setLocation(event):
    keyword = "!Default Location: "
    description = event.description
    if(description == None or keyword not in description):
        return getUserLocation()
    else:
        return description.split(keyword,1)[1].split('!',1)[0].strip()
    
gc = GoogleCalendar(credentials_path='.credentials/credentials.json', save_token=True)
events = gc.get_events(order_by='startTime', single_events=True, time_min=D.now(), time_max=D.now() + 7*days)
upcomingEvent = next(events)
upcomingEventDescription = upcomingEvent.description
if datetime.now(pytz.utc) > upcomingEvent.start:
    upcomingEvent = next(events)
userLocation = setLocation(upcomingEvent)
eventLocation = upcomingEvent.location
travelTime = get_directions(userLocation, eventLocation)
variation = setVariation(upcomingEvent)
addReminder(upcomingEvent, travelTime + variation)
if eventLocation == None:
    print("Could not get event location.")
    eventLocation = "None"
print(f"{userLocation} to {eventLocation} will take {travelTime} minutes. You will be notified {variation} minutes before you have to leave.")

# To choose additional time, user must follow the following format
# !Extra Time: (# of minutes)
# To set the user's location for an event, user must follow the following format
# !Default Location: (Address of location)