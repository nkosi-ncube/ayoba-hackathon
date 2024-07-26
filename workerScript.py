# your_worker_script.py
from gatewayapi.tokenManager import token_manager
import requests

from gatewayapi.tokenManager import token_manager
import requests

def make_authenticated_request(url, data=None):
    token = token_manager.get_token()
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None
    except Exception as err:
        print(f"Other error occurred: {err}")
        return None

# Example usage of the authenticated request
if __name__ == "__main__":
    print("Workser script  is running  on the server")
    url = "https://api.ayoba.me/v1/business/avatar/get-slot"
    data = {  "fileName": "awesome-selfy.jpeg"}

    response = make_authenticated_request(url, data)

    print(response)
