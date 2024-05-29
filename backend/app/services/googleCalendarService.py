import requests
from flask import current_app as app
from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event
from gcsa.reminders import EmailReminder, PopupReminder
import re
from datetime import datetime
import pytz
from beautiful_date import *

class GoogleCalendarService:
    def __init__(self):
        self.gc = GoogleCalendar(credentials_path=app.config['CREDENTIALS_PATH'], save_token=True)

    def get_user_location(self):
        params = {'key': app.config['GOOGLE_API_KEY']}
        response = requests.post('https://www.googleapis.com/geolocation/v1/geolocate', params=params)
        json = response.json()
        if 'location' in json:
            coordinates = json['location']
            params = {
                'latlng': f"{coordinates['lat']},{coordinates['lng']}",
                'key': app.config['GOOGLE_API_KEY']
            }
            response = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=params)
            json = response.json()
            if 'results' in json and len(json['results']) > 0:
                return json['results'][0]['formatted_address']
            else:
                return "Error: Something went wrong. Could not get user address."
        else:
            return "Error: Something went wrong. Could not get location in json."

    def get_location(self, address):
        params = {'address': address, 'key': app.config['GOOGLE_API_KEY']}
        response = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=params)
        json = response.json()
        if 'results' in json and len(json['results']) > 0:
            return json['results'][0]['geometry']['location']
        else:
            return "Error: Something went wrong. Could not get location from address."

    def get_directions(self, origin, destination):
        params = {'origin': origin, 'destination': destination, 'key': app.config['GOOGLE_API_KEY']}
        response = requests.get('https://maps.googleapis.com/maps/api/directions/json', params=params)
        json = response.json()
        if 'routes' in json and len(json['routes']) > 0:
            seconds = json['routes'][0]['legs'][0]['duration']['value']
            return round(seconds / 60)
        else:
            return 0

    def run(self):
        events = self.gc.get_events(order_by='startTime', single_events=True, time_min=D.now(), time_max=D.now() + 7*days)
        upcoming_event = next(events)
        if datetime.now(pytz.utc) > upcoming_event.start:
            upcoming_event = next(events)
        user_location = self.set_location(upcoming_event)
        event_location = upcoming_event.location
        travel_time = self.get_directions(user_location, event_location)
        variation = self.set_variation(upcoming_event)
        self.add_reminder(upcoming_event, travel_time + variation)
        if event_location == None:
            event_location = "None"
        return f"Success: {user_location} to {event_location} will take {travel_time} minutes. You will be notified {variation} minutes before you have to leave."

    def set_variation(self, event):
        keyword = "!Extra Time: "
        description = event.description
        if not description or keyword not in description:
            return 0
        else:
            variation = re.search(f'{keyword}(.*?)!', description)
            if variation:
                return int(variation.group(1).strip())
            else:
                return -1000

    def set_location(self, event):
        keyword = "!Default Location: "
        description = event.description
        if not description or keyword not in description:
            return self.get_user_location()
        else:
            location = re.search(f'{keyword}(.*?)!', description)
            location = re.sub('<.*?>', '', location.group(1))
            if location:
                return location.strip()
            else:
                return "Error: Could not get location from event description."

    def add_reminder(self, event, reminder):
        email_reminder = EmailReminder(minutes_before_start=reminder)
        popup_reminder = PopupReminder(minutes_before_start=reminder)
        updated_event = Event(
            event.summary,
            start=event.start,
            end=event.end,
            description=event.description,
            location=event.location,
            reminders=[email_reminder, popup_reminder],
            event_id=event.event_id
        )
        self.gc.update_event(updated_event)
