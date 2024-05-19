from flask import Blueprint, jsonify
from ..services.googleCalendarService import GoogleCalendarService

authBP = Blueprint('authBP', __name__)
gcService = GoogleCalendarService()

@authBP.route('/login', methods=['POST'])
def login_route():
    gcService.login()
    return jsonify({'message': 'Login successful'})
