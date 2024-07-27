
from retry_requests import retry
from requests import Session
def translate_text(text,choice ):
    TRANSLATION_URL = "https://vulavula-services.lelapa.ai/api/v1/translate/process"
    VULAVULA_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY1NDQxNGJmMzNkMzQ5OTQ4Mjg2MmM4OGM5MzM1MTI5IiwiY2xpZW50X2lkIjo5NywicmVxdWVzdHNfcGVyX21pbnV0ZSI6MCwibGFzdF9yZXF1ZXN0X3RpbWUiOm51bGx9.6j9Vjj_9GTkw_TS27Huv9Wf8TtMtJjXKUd6CbFTl7vc"

    headers={
        "X-CLIENT-TOKEN": VULAVULA_TOKEN,
    }

    # Get retry helper session
    session = retry(Session(), retries=10, backoff_factor=1)

    payload = {
    "input_text": text,
    "source_lang": "eng_Latn",
    "target_lang": choice,
    
    }

    translation_resp = session.post(
        TRANSLATION_URL,
        json=payload,
        headers=headers,
    )

    return translation_resp.json().get("translation")[0].get("translation_text")


if __name__ == "__main__":
    print(translate_text("""Dont worry about the female voice its my robot that knows how to change english to sesotho.Is the Sotho good""", "sot_Latn"))
    print("done")