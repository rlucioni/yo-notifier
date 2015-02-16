# We need to import request to access the details of the POST request
from flask import Flask, request
# We need to import requests to make the call to the Yo API
import requests
import os
import json


INFOSNIPER_BASE_URL = 'http://www.infosniper.net/index.php?ip_address='
YO_API_ENDPOINT = 'https://api.justyo.co/yo/'


# Initialize the Flask application
app = Flask(__name__)

@app.route('/payload', methods=['POST'])
def handle_hook():
    data = request.get_json()
    event_name = data['event']
    geolocation_link = INFOSNIPER_BASE_URL + data['context']['ip']

    if event_name == 'profile.viewed':
        if data['properties']['id'] == 'github':
            # Send a Yo from YO_API_TOKEN account to TARGET_USERNAME
            requests.post(YO_API_ENDPOINT, data={
                'api_token': str(os.environ.get('YO_API_TOKEN_GITHUBPROFILEVIEWED')),
                'username': str(os.environ.get('TARGET_USERNAME')),
                'link': geolocation_link
            })

            return "Yo sent!"
        else:
            return "Nothing to do."
    elif event_name == 'project.viewed':
        requests.post(YO_API_ENDPOINT, data={
            'api_token': str(os.environ.get('YO_API_TOKEN_PROJECTVIEWED')),
            'username': str(os.environ.get('TARGET_USERNAME')),
            'link': geolocation_link
        })

        return "Yo sent!"
    elif event_name == 'resume.viewed':
        requests.post(YO_API_ENDPOINT, data={
            'api_token': str(os.environ.get('YO_API_TOKEN_RESUMEVIEWED')),
            'username': str(os.environ.get('TARGET_USERNAME')),
            'link': geolocation_link
        })

        return "Yo sent!"
    else:
        return "Nothing to do."


# Run the app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
