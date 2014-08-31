# We need to import request to access the details of the POST request
from flask import Flask, request
# We need to import requests to make the call to the Yo API
import requests
import os
import json

API_TOKEN = '9f1270af-67a9-4574-99db-1c58503ea165'
USERNAME = "rlucioni"

# Initialize the Flask application
app = Flask(__name__)

@app.route('/payload', methods=['POST'])
def handle_hook():
    data = request.get_json()
    if data['event'] == 'resume.viewed':
        # Send a Yo from API_TOKEN account to USERNAME
        requests.post('https://api.justyo.co/yo/', data={'api_token': API_TOKEN, "username": USERNAME})
        return "Yo sent!"
    else:
        return "Nothing to do."

# Run the app
if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
