import os
import requests
import threading

class AyobaTokenManager:
    def __init__(self):
        self.username = os.getenv('AYOBA_USERNAME')
        self.password = os.getenv('AYOBA_PASSWORD')
        self.token = None
        self.token_lock = threading.Lock()
        self.refresh_token()

    def refresh_token(self):
        def login_to_ayoba():
            url = "https://api.ayoba.me/v2/login"
            print(self.username , self.password)
            payload = {
                "username": self.username,
                "password": self.password
            }
            headers = {
                'Content-Type': 'application/json'
            }
            try:
                response = requests.post(url, headers=headers, json=payload)
                response.raise_for_status()
                return response.json().get('token')  # Adjust according to the actual response structure
            except requests.exceptions.HTTPError as http_err:
                print(f"HTTP error occurred: {http_err}")
                return None
            except Exception as err:
                print(f"Other error occurred: {err}")
                return None

        with self.token_lock:
            self.token = login_to_ayoba()
            print(f"New token: {self.token}")

        # Schedule the next token refresh
        threading.Timer(1800, self.refresh_token).start()  # Refresh every 30 minutes

    def get_token(self):
        with self.token_lock:
            return self.token

# Create a singleton instance of AyobaTokenManager
token_manager = AyobaTokenManager()
