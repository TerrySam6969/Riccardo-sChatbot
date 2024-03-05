import requests
import json

def translateText(text):
    url = "https://google-translation-unlimited.p.rapidapi.com/translate"

    payload = {
        "texte": text,
        "to_lang": "pt"
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "bbb1b7e1b0mshe1d514534c44611p12a24fjsn5dc5afaf6c43",
        "X-RapidAPI-Host": "google-translation-unlimited.p.rapidapi.com"
    }

    try:
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        response = json.loads(response.content)
        translation = response.get('translation_data', {}).get('translation')
        return(translation)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the translation: {e}")

translateText("hello")
