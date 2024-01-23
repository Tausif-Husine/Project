import requests

CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"

headers = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": "8270c2e3e2abf3015bd98b638bc62555"
}

data = {
  "text": "Born and raised in the charming south, I can add a touch of sweet southern hospitality to your audiobooks and podcasts",
  "model_id": "eleven_multilingual_v2",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.5
  }
}

response = requests.post(url, json=data, headers=headers)

#print(response.json())
if response.status_code == 200:
	print("Successfull")
else:
	print("failed")

with open('output.mp3', 'wb') as f:
    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            f.write(chunk)
            