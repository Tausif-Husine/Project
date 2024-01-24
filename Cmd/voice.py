import requests
from pathlib import Path

CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"

headers = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": ""
}

def tts(prompt):
  data = {
  "text": prompt,
  "model_id": "eleven_multilingual_v2",
  "voice_settings": {
  "stability": 0.5,
  "similarity_boost": 0.5
  }
  }
  response = requests.post(url, json=data, headers=headers)
  
  filename = 'Cmd/Cache/my.mp3'
  
  with open(Path(filename), 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
            	f.write(chunk)
  return filename           