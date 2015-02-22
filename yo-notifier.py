import os
import json

# We need to import request to access the details of the POST request
from flask import Flask, request
# We need to import requests to make the call to the Yo API
import requests
from bs4 import BeautifulSoup as bs


INFOSNIPER_BASE_URL = 'http://www.infosniper.net/index.php?ip_address='
YO_API_ENDPOINT = 'https://api.justyo.co/yo/'


# Initialize the Flask application
app = Flask(__name__)


def send_yo(api_token, username, link=None, location=None):
    """POST the Yo endpoint with the provided data.
    
    Sends a Yo from the account corresponding to the provided API token to the account
    corresponding to the specified username.

    Location must be a string formatted as 'latitude;longitude'.
    """
    data = {
        'api_token': api_token,
        'username': username
    }

    if link:
        data['link'] = link
    elif location:
        data['location'] = location

    response = requests.post(YO_API_ENDPOINT, data=data)

    if response.status_code == 200:
        return "Yo sent!"
    else:
        # Try to alert the target user of the failure by sending a
        # notification from a separate account.
        requests.post(YO_API_ENDPOINT, data={
            'api_token': str(os.environ.get('YO_API_TOKEN_NOTIFIERERROR')),
            'username': username
        })

        return "Unable to send notification."


@app.route('/notify', methods=['POST'])
def handle_hook():
    data = request.get_json()
    event_name = data['event']
    geolocation_link = INFOSNIPER_BASE_URL + data['context']['ip']

    if str(os.environ.get('SEND_NOTIFICATIONS')) == 'True':
        if event_name == 'profile.viewed':
            if data['properties']['id'] == 'github':
                return send_yo(
                    str(os.environ.get('YO_API_TOKEN_GITHUBPROFILEVIEWED')),
                    str(os.environ.get('TARGET_USERNAME')),
                    link=geolocation_link
                )
            else:
                return "Nothing to do."
        elif event_name == 'project.viewed':
            return send_yo(
                str(os.environ.get('YO_API_TOKEN_PROJECTVIEWED')),
                str(os.environ.get('TARGET_USERNAME')),
                link=geolocation_link
            )
        elif event_name == 'resume.viewed':
            return send_yo(
                str(os.environ.get('YO_API_TOKEN_RESUMEVIEWED')),
                str(os.environ.get('TARGET_USERNAME')),
                link=geolocation_link
            )
        else:
            return "Nothing to do."
    else:
        return "Notifications disabled."


# Run the app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
