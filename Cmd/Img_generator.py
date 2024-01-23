from pathlib import Path
import requests
import json
import time

url = "https://api.prodia.com/v1/sd/generate"
job_url_template = "https://api.prodia.com/v1/job/{}"

directory = Path('Cmd/Cache')

def generateImg(prompt):
    payload = {
        "prompt": "Somethings ",
        "model": "anythingV5_PrtRE.safetensors [893e49b9]",
        "negative_prompt": "badly drawn",
        "steps": 20,
        "cfg_scale": 7,
        "seed": -1,
        "upscale": True,
        "sampler": "DPM++ 2M Karras"
    }
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-Prodia-Key": "e92f070f-56ab-46fa-9a61-1e711d20da24"
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        jobid = data['job']
        time.sleep(10)        
        job_url = job_url_template.format(jobid)
        headers_job = {
            "accept": "application/json",
            "X-Prodia-Key": "e92f070f-56ab-46fa-9a61-1e711d20da24"
        }
        
        img = requests.get(job_url, headers=headers_job)
        
        if img.status_code == 200:
            img_data = img.json()
            img_url = img_data['imageUrl']
            download_img = requests.get(img_url)
            
            if download_img.status_code == 200:
            	filename = directory / Path(img_url).name
            	with open(filename, "wb") as file:
            		file.write(download_img.content)
            		return filename
        else:
            return f'Error: {img.status_code}'
    else:
        return f'Error: {response.status_code}'