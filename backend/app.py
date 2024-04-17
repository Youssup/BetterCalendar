# Importing flask
from flask import Flask, request, jsonify, redirect

# Imports for application functionality
# API calls
import requests
# API key
import config as config
# For adjusting time
import pytz
# regex for parsing event description
import re

# GCSA API for Google Calendar integration + time manipulation
from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event
from gcsa.reminders import EmailReminder, PopupReminder
from beautiful_date import *
from datetime import datetime

app = Flask(__name__)
gc = None

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
def getDirections(origin, destination):
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
        print("Error: Could not get location from event.")
        return 0

# Add reminder to event
def addReminder(event, reminder):
    emailReminder = EmailReminder(minutes_before_start=reminder)
    popupReminder = PopupReminder(minutes_before_start=reminder)
    updatedEvent = Event(
        event.summary,
        start=event.start,
        end=event.end,
        description=event.description,
        location=event.location,
        reminders=[emailReminder, popupReminder],
        event_id=event.event_id
    )
    gc.update_event(updatedEvent)

# Parse event's description to find user variation
def setVariation(event):
    keyword = "!Extra Time: "
    description = event.description
    if (description == None or keyword not in description):
        return 0
    else:
        variation = re.search(f'{keyword}(.*?)!', description)
        if variation:
            return int(variation.group(1).strip())
        else:
            return -1000

# Sets the user's location
def setLocation(event):
    keyword = "!Default Location: "
    description = event.description
    if (description == None or keyword not in description):
        return getUserLocation()
    else:
        location = re.search(f'{keyword}(.*?)!', description)
        location = re.sub('<.*?>', '', location.group(1))
        if location:
            return location.strip()
        else:
            return "Error: Could not get location from event description."

@app.route('/', methods=['GET'])
def homeRoute():
    return "test"

@app.route('/login', methods=['GET'])
def loginRoute():
    global gc
    gc = GoogleCalendar(credentials_path='.credentials/credentials.json', save_token=True)
    return jsonify({'message': 'Login successful'})

# Gets the user's location
@app.route('/getUserLocation', methods=['GET'])
def getUserLocationRoute():
    return jsonify(getUserLocation())
    
# Gets the longitude and latitude values of the address
@app.route('/getLocation', methods=['GET'])
def getLocationRoute():
    return jsonify(getLocation())
    
# Gets the travel time from the user's location to the event location
@app.route('/getDirections', methods=['GET'])
def getDirectionsRoute():
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    return jsonify(getDirections(origin, destination))

@app.route('/addReminder', methods=['GET'])
def addReminderRoute():
    event = request.args.get('event')
    reminder = request.args.get('reminder')
    return jsonify(addReminder(event, reminder))

@app.route('/setVariation', methods=['GET'])
def setVariationRoute():
    event = request.args.get('event')
    return jsonify(setVariation(event))

@app.route('/setLocation', methods=['GET'])
def setLocationRoute():
    event = request.args.get('event')
    return jsonify(setLocation(event))

@app.route('/run', methods=['GET'])
def runRoute():
    events = gc.get_events(order_by='startTime', single_events=True,time_min=D.now(), time_max=D.now() + 7*days)
    upcomingEvent = next(events)
    upcomingEventDescription = upcomingEvent.description
    if datetime.now(pytz.utc) > upcomingEvent.start:
        upcomingEvent = next(events)
    userLocation = setLocation(upcomingEvent)
    eventLocation = upcomingEvent.location
    travelTime = getDirections(userLocation, eventLocation)
    variation = setVariation(upcomingEvent)
    addReminder(upcomingEvent, travelTime + variation)
    if eventLocation == None:
        return jsonify("Error: Could not get event location.")
    return jsonify(f"Success: {userLocation} to {eventLocation} will take {travelTime} minutes. You will be notified {variation} minutes before you have to leave.")

if __name__ == '__main__':
    app.run(debug=True)
