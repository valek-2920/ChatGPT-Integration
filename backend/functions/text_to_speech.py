import requests
from decouple import config

ELEVEN_LABS_API_KEY = config("ELEVEN_LABS_API_KEY")
GLENDA_VOICE_ID = config("GLENDA_VOICE_ID")


def convert_text_to_speech(message):

    body = {
        "text": message,
        "voice_settings": {
            "stability": 0,
            "similarity_boost": 0,
            "style": 0,
            "use_speaker_boost": True,
        }
    }

    headers = {
        "xi-api-key": ELEVEN_LABS_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{GLENDA_VOICE_ID}"

    try:
        response = requests.post(url=url, json=body, headers=headers)
    except Exception as e:
        print(e)
        return

    print(response)

    if response.status_code == 200:
        return response.content
    else:
        return
