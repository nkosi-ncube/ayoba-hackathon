import os
import requests
import threading

class AyobaTokenManager:
    def __init__(self):
        self.username = os.getenv('AYOBA_USERNAME')
        self.password = os.getenv('AYOBA_PASSWORD')
        
        # Debugging: print environment variables to check if they are being read correctly
        print(f"AYOBA_USERNAME: {self.username}")
        print(f"AYOBA_PASSWORD: {self.password}")
        
        self.token = None
        self.token_lock = threading.Lock()
        self.refresh_token()

    def refresh_token(self):
        def login_to_ayoba():
            url = "https://api.ayoba.me/v2/login"
            print(f"Attempting login with username: {self.username}")
            payload = {
                "username": self.username,
                "password": self.password
            }
            headers = {
                'Content-Type': 'application/json'
            }
            try:
                response = requests.post(url, headers=headers, json=payload)
                print(f"Response status code: {response.status_code}")
                print(f"Response content: {response.text}")
                response.raise_for_status()
                token = response.json().get('token')
                print(f"Token received: {token}")
                return token
            except requests.exceptions.HTTPError as http_err:
                print(f"HTTP error occurred: {http_err}")
                return None
            except Exception as err:
                print(f"Other error occurred: {err}")
                return None

        with self.token_lock:
            new_token = login_to_ayoba()
            if new_token:
                self.token = new_token
                print(f"New token: {self.token}")
            else:
                print("Failed to get a new token")

        # Schedule the next token refresh
        threading.Timer(1800, self.refresh_token).start()  # Refresh every 30 minutes

    def get_token(self):
        with self.token_lock:
            return self.token

# Create a singleton instance of AyobaTokenManager
token_manager = AyobaTokenManager()
print("Token Manager instance created:", token_manager)
print("Initial token:", token_manager.get_token())