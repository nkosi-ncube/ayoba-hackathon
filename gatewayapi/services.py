import requests
from django.conf import settings
from .models import Message

from .tokenManager import token_manager
# jwt_token = login_to_ayoba(username, password)
# jwt_token = login_to_ayoba(username, password)
access_token= token = token_manager.get_token()
AYOBA_API_URL="https://api.ayoba.me"
def send_message(msisdns, message_type, message_text):
    url = f"{AYOBA_API_URL}/v1/business/message"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    payload = {
        "msisdns": msisdns,
        "message": {
            "type": message_type,
            "text": message_text
        }
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"error": f"Other error occurred: {err}"}
    return response.json()
  # Import the Message model from your app
 # Make sure to import settings if needed

def get_message(msisdns, message_type, message_text):
    url = f"{AYOBA_API_URL}/v1/business/message"
    headers = {
        'Authorization': f'Bearer {access_token}',  # Ensure you have ACCESS_TOKEN in your settings
        'Content-Type': 'application/json',
    }
    payload = {
        "msisdns": msisdns,
        "message": {
            "type": message_type,
            "text": message_text
        }
    }
    try:
        response = requests.get(url, headers=headers, json=payload)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"error": f"Other error occurred: {err}"}
    
    response_data = response.json()

    if response_data:
        for message_data in response_data:
            msisdn = message_data.get('msisdn')
            message_id = message_data.get('messageId')
            message_info = message_data.get('message', {})
            from_jid = message_info.get('fromJid', '')
            message_type = message_info.get('type', '')
            text = message_info.get('text', '')
            url = message_info.get('url', '')

            message = Message(
                msisdn=msisdn,
                message_id=message_id,
                from_jid=from_jid,
                message_type=message_type,
                text=text,
                url=url,
            )
            message.save()
    
    return response_data


def send_file_message(msisdns, file_url):
    url = f"{AYOBA_API_URL}/v1/business/message/file"
    headers = {
        'Authorization': f'Bearer {settings.AYOBA_API_KEY}',
        'Content-Type': 'application/json',
    }
    payload = {
        "msisdns": msisdns,
        "file_url": file_url
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"error": f"Other error occurred: {err}"}
    return response.json()

def get_media_slots():
    url = f"{AYOBA_API_URL}/v1/business/message/media/get-slots"
    headers = {
        'Authorization': f'Bearer {settings.AYOBA_API_KEY}',
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"error": f"Other error occurred: {err}"}
    return response.json()

def get_avatar_slot():
    url = f"{AYOBA_API_URL}/v1/business/avatar/get-slot"
    headers = {
        'Authorization': f'Bearer {settings.AYOBA_API_KEY}',
    }
    try:
        response = requests.get(url, headers=headers) 
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"error": f"Other error occurred: {err}"}
    return response.json()
