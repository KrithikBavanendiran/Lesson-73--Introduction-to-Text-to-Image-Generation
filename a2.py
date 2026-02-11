from config import HF_API_KEY
import requests
import base64
from PIL import Image
from io import BytesIO

URL = "https://api.stability.ai/v2beta/stable-image/generate/core"

while True:
    prompt = input("\nEnter image prompt (or type exit): ")
    
    if prompt.lower() == "exit":
        print("Goodbye!")
        break

    headers = {"Authorization": f"Bearer {HF_API_KEY}","Accept": "application/json"}

    files = {"prompt": (None, prompt),"output_format": (None, "png")}
    print("\nGenerating image...\n")
    response = requests.post(URL, headers=headers, files=files)

    if response.status_code != 200:
        print("Error:", response.text)
        continue

    data = response.json()
    image_base64 = data["image"]
    image_bytes = base64.b64decode(image_base64)
    image = Image.open(BytesIO(image_bytes))
    image.show()
    save = input("Do you want to save it? (yes/no): ")

    if save.lower() == "yes":
        name = input("Enter filename: ") or "generated_image"
        image.save(f"{name}.png")
        print("Image saved successfully!")