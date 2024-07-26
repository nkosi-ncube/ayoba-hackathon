import requests
from django.conf import settings
from .models import Message

access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IjliNTIwMGU1M2JjMGU2NDczYzllMzIyZDMwYjA2Yjk0MjZmYzEyY2IiLCJqaWQiOiI5YjUyMDBlNTNiYzBlNjQ3M2M5ZTMyMmQzMGIwNmI5NDI2ZmMxMmNiQGF5b2JhLm1lIiwiZ3JvdXAiOiJidXNpbmVzcyIsIm1zaXNkbiI6bnVsbCwiaWF0IjoxNzIyMDA5OTY0LCJleHAiOjE3MjIwMTE3NjR9.gtuTStDNNpWFec82tXpeVxG66kZeX-2j523MwLpXsis"
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
            message_id = message_data['messageId']
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
