# We need to import request to access the details of the POST request
from flask import Flask, request
# We need to import requests to make the call to the Yo API
import requests
import os
import json


BASE_URL = 'http://www.infosniper.net/index.php?ip_address='


# Initialize the Flask application
app = Flask(__name__)

@app.route('/payload', methods=['POST'])
def handle_hook():
    data = request.get_json()
    if data['event'] == 'resume.viewed':
        link = BASE_URL + data['context']['ip']
        # Send a Yo from YO_API_TOKEN account to USERNAME
        requests.post('https://api.justyo.co/yo/', data={
            'api_token': str(os.environ.get('YO_API_TOKEN')),
            'username': str(os.environ.get('TARGET_USERNAME')),
            'link': link
        })
        return "Yo sent!"
    else:
        return "Nothing to do."


# Run the app
if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
