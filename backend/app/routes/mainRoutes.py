from flask import Blueprint, jsonify, request
from ..services.googleCalendarService import GoogleCalendarService

mainBP = Blueprint('mainBP', __name__)
gcService = GoogleCalendarService()

@mainBP.route('/', methods=['GET'])
def test():
    return "test"

@mainBP.route('/getUserLocation', methods=['GET'])
def get_user_location_route():
    return jsonify(gcService.get_user_location())

@mainBP.route('/getLocation', methods=['GET'])
def get_location_route():
    address = request.args.get('address')
    return jsonify(gcService.get_location(address))

@mainBP.route('/getDirections', methods=['GET'])
def get_directions_route():
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    return jsonify(gcService.get_directions(origin, destination))

@mainBP.route('/runOnGoogle', methods=['GET'])
def run_on_google_route():
    return gcService.runOnGoogle()

@mainBP.route('/runOnApp', methods=['GET'])
def run_on_app_route():
    variation = request.args.get('variation')
    defaultLocation = request.args.get('defaultLocation')
    return gcService.runOnApp(variation, defaultLocation)
