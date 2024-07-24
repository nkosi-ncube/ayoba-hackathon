import requests
from django.conf import settings

def send_message(msisdns, message_type, message_text):
    url = f"{settings.AYOBA_API_URL}/v1/business/message"
    headers = {
        'Authorization': f'Bearer {settings.AYOBA_API_KEY}',
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

def send_file_message(msisdns, file_url):
    url = f"{settings.AYOBA_API_URL}/v1/business/message/file"
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
    url = f"{settings.AYOBA_API_URL}/v1/business/message/media/get-slots"
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
    url = f"{settings.AYOBA_API_URL}/v1/business/avatar/get-slot"
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
