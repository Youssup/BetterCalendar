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

@mainBP.route('/run', methods=['GET'])
def run_route():
    return gcService.run()
