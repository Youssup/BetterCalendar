import config
import requests

from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event
from gcsa.reminders import EmailReminder, PopupReminder
from beautiful_date import *

# Get location the user
def get_user_location():
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
            print("Error: Something went wrong" + json)
            return None
    else:
        print("Error: Something went wrong" + json)
        return None 

# Get travel time
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
        print("Error: Something went wrong" + json)
        return None

# Add reminder to event
def addReminder(event, reminder):
    event.reminders = [EmailReminder(minutes_before_start=reminder), PopupReminder(minutes_before_start=reminder)]
    gc.update_event(event)
    
gc = GoogleCalendar(credentials_path='.credentials/credentials.json', save_token=True)
events = gc.get_events(order_by='startTime', single_events=True, time_min=D.now(), time_max=D.now() + 7*days)
upcomingEvent = next(events)
userLocation = get_user_location()
eventLocation = upcomingEvent.location
travelTime = get_directions(userLocation, eventLocation)
variation = 0 # Will be user's input once I have a front end
addReminder(upcomingEvent, travelTime + variation)
print(userLocation + " to " + eventLocation + " will take " + str(travelTime) + " minutes. You will be notified " + str(variation) + " minutes before you have to leave.")