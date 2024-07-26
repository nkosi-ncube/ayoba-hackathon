import requests


def login_to_ayoba(username, password):
    url = "https://api.ayoba.me/v2/login"
    payload = {
        "username": username,
        "password":password
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(response.text)
        response.raise_for_status()
        return response.json().get('token')  # Adjust according to the actual response structure
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None
    except Exception as err:
        print(f"Other error occurred: {err}")
        return None

# Usage
username = "9b5200e53bc0e6473c9e322d30b06b9426fc12cb"
password =  "tg6JBhaNnIy8D8t62Tq74H3lfoOGzVz"
jwt_token = login_to_ayoba(username, password)
# access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IjliNTIwMGU1M2JjMGU2NDczYzllMzIyZDMwYjA2Yjk0MjZmYzEyY2IiLCJqaWQiOiI5YjUyMDBlNTNiYzBlNjQ3M2M5ZTMyMmQzMGIwNmI5NDI2ZmMxMmNiQGF5b2JhLm1lIiwiZ3JvdXAiOiJidXNpbmVzcyIsIm1zaXNkbiI6bnVsbCwiaWF0IjoxNzIxOTk2MjQ3LCJleHAiOjE3MjE5OTgwNDd9.v0Xf8xwEZN51_RuI3NBkzqADRRMID-8LuXUT5RiIxf0"
# def send_message(msisdns, message_type, message_text):
#     url = "https://api.ayoba.me/v1/business/message"
#     headers = {
#         'Authorization': f'Bearer {access_token}',
#         'Content-Type': 'application/json',
#     }
#     payload = {
#         "msisdns": msisdns,
#         "message": {
#             "type": message_type,
#             "text": message_text
#         }
#     }
#     try:
#         response = requests.get(url, headers=headers, json=payload)
#         print(response.text)
#         response.raise_for_status()
#     except requests.exceptions.HTTPError as http_err:
#         return {"error": f"HTTP error occurred: {http_err}"}
#     except Exception as err:
#         return {"error": f"Other error occurred: {err}"}
#     return response.json()

# print(send_message(["+27648917936"], "text", "hello"))