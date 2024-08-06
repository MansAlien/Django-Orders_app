import os
import requests

def download_image(url, save_path):
    try:
        # Expand the user's home directory
        save_path = os.path.expanduser(save_path)
        
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check if the request was successful

        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Image successfully downloaded: {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download image: {e}")

# Example usage
image_url = "http://192.168.1.16:9000/media/files/2024-08-04-174710_hyprshot.png"
save_path = "~/Downloads/2024-08-04-174710_hyprshot.png"
download_image(image_url, save_path)

