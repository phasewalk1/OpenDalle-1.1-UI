import requests
from dotenv import load_dotenv
import os
import sys
import io
from PIL import Image

def query(api_url, headers, prompt):
    response = requests.post(api_url, headers=headers, json={"inputs": prompt})
    return response.content

def main(prompt):
    load_dotenv()
    HF_API_TOKEN = os.getenv('HF_API_TOKEN')

    API_URL = "https://api-inference.huggingface.co/models/dataautogpt3/OpenDalleV1.1"
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

    image_bytes = query(API_URL, headers, prompt)

    # Load the image from bytes and save it
    image = Image.open(io.BytesIO(image_bytes))
    image.save("image.png")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py 'prompt'")
        sys.exit(1)

    prompt = sys.argv[1]
    main(prompt)
