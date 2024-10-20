import requests
from django.conf import settings


def get_bkash_token():
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "username": "01770618567",
        "password": "D7DaC<*E*eG"
    }

    # Define the body
    data = {
        "app_key": "0vWQuCRGiUX7EPVjQDr0EUAYtc",
        "app_secret": "jcUNPBgbcqEDedNKdvE4G1cAK7D3hCjmJccNPZZBq96QIxxwAMEx"
    }

    try:
        # Make the request to the external API using requests
        response = requests.post(
            "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/token/grant",
            json=data,
            headers=headers
        )

        # Check if the response is successful
        if response.status_code == 200:
            return response.json()['id_token']
        elif response.status_code == 401:
            return None
        else:
            return None

    except requests.exceptions.RequestException as e:
        return None