import requests
from PIL import Image
from io import BytesIO
from config import HF_API_KEY

API_URL="https://api.stability.ai/v1/generation/{engine_id}/text-to-image"

def generate_image_from_text(prompt: str) -> Image.Image:
    headers={"Authorization": f"Bearer {HF_API_KEY}"}
    payload={"inputs": prompt}

    try:
        response=requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()

        if 'image' in response.headers.get('Content-Type', ''):
            image=Image.open(BytesIO(response.content))
            return image
        else:
            raise Exception("Unexpected response format: Expected an image.")
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {e}")
    
def main():
    """Main loop for user interaction. Continuosly prompts the user for a text description, generates an image via the API, and displays, and offers the option to save the image."""
    print("Welcome to the Text to Image Generator!")
    print("Type 'exit' to quit the program.\n")
    while True:
        prompt=input("Enter a text description for the image you want to generate:\n ").strip()
        if prompt.lower() == 'exit':
            print("Goodbye!")
            break

        print("\nGenerating image...\n")
        try:
            image= generate_image_from_text(prompt)
            image.show()

            save_option=input("Do you want to save the image? (yes/no): ").strip().lower()
            if save_option == 'yes':
                file_name=input("Enter a name for the image file (without extension)").strip() or "generated_image"
                image.save(f"{file_name}.png")
                print(f"Image saved as {file_name}.png\n")
        except Exception as e:
            print(f"An error occured: {e}\n")
        
        print("-" * 80 + "\n")
if __name__ == "__main__":
    main()  