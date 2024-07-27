import os
from retry_requests import retry
from requests import Session

def translate_text(text, choice):
    TRANSLATION_URL = "https://vulavula-services.lelapa.ai/api/v1/translate/process"
    VULAVULA_TOKEN = os.getenv("VULAVULA_TOKEN")

    if not VULAVULA_TOKEN:
        raise ValueError("VULAVULA_TOKEN environment variable not set")

    headers = {
        "X-CLIENT-TOKEN": VULAVULA_TOKEN,
    }

    session = retry(Session(), retries=3, backoff_factor=1)

    payload = {
        "input_text": text,
        "source_lang": "eng_Latn",
        "target_lang": choice,
    }

    try:
        translation_resp = session.post(
            TRANSLATION_URL,
            json=payload,
            headers=headers,
        )
        translation_resp.raise_for_status()

        translation_data = translation_resp.json()
        translation_text = translation_data.get("translation", [{}])[0].get("translation_text", "No translation found")

        return translation_text
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return "Translation failed due to HTTP error"
    except Exception as err:
        print(f"Other error occurred: {err}")
        return "Translation failed due to an error"

if __name__ == "__main__":
    translated_text = translate_text(
        "Don't worry about the female voice; it's my robot that knows how to change English to Sesotho. Is the Sotho good?",
        "sot_Latn"
    )
    print(translated_text)
    print("done")
