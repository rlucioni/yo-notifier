import os
import re
from functools import partial

import requests
from flask import Flask, request
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


def parse_coordinates(infosniper_link):
    """Parse the page to extract coordinates and return a string 'latitude;longitude'.

    If unable to parse both required coordinates, return the provided link, unchanged.
    """
    response = requests.get(infosniper_link)
    soup = bs(response.content)
    
    # Find the two table cells containing coordinates
    cells = soup.find_all(class_='content-td2', text=re.compile('-*\d+\.\d+'), limit=2)

    if len(cells) == 2:
        # Construct the location string expected by the Yo API
        coordinate_string = '{latitude};{longitude}'.format(latitude=cells[0].string, longitude=cells[1].string)
        return {'type': 'coordinates', 'content': coordinate_string}
    else:
        # Fall back to the raw link
        return {'type': 'link', 'content': infosniper_link}


@app.route('/notify', methods=['POST'])
def notify():
    data = request.get_json()
    event_name = data['event']
    infosniper_link = INFOSNIPER_BASE_URL + data['context']['ip']

    parsed = parse_coordinates(infosniper_link)
    if parsed['type'] == 'coordinates':
        yo_from = partial(send_yo, username=str(os.environ.get('TARGET_USERNAME')), location=parsed['content'])
    else:
        yo_from = partial(send_yo, username=str(os.environ.get('TARGET_USERNAME')), link=parsed['content'])

    if str(os.environ.get('SEND_NOTIFICATIONS')) == 'True':
        if event_name == 'profile.viewed':
            if data['properties']['id'] == 'github':
                return yo_from(str(os.environ.get('YO_API_TOKEN_GITHUBPROFILEVIEWED')))
            else:
                return "Nothing to do."
        elif event_name == 'project.viewed':
            return yo_from(str(os.environ.get('YO_API_TOKEN_PROJECTVIEWED')))
        elif event_name == 'resume.viewed':
            return yo_from(str(os.environ.get('YO_API_TOKEN_RESUMEVIEWED')))
        else:
            return "Nothing to do."
    else:
        return "Notifications disabled."


# Run the app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
