# We need to import request to access the details of the POST request
from flask import Flask, request
# We need to import requests to make the call to the Yo API
import requests
import sys
 
HOST_NAME = sys.argv[1]
PORT_NUMBER = int(sys.argv[2])

API_TOKEN = '9f1270af-67a9-4574-99db-1c58503ea165'
USERNAME = "rlucioni"

# Initialize the Flask application
app = Flask(__name__)

@app.route('/payload', methods=['POST'])
def handle_hook():
    data = request.get_json()
    if data['event'] == 'resume.viewed':
        # Send a Yo from API_TOKEN account to USERNAME
        response = requests.post('https://api.justyo.co/yo/', data={'api_token': API_TOKEN, "username": USERNAME})
        print response

# Run the app
if __name__ == '__main__':
    app.run(host=HOST_NAME, port=PORT_NUMBER)
