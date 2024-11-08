import requests


def upload_image_to_imgur(image_file, client_id):
    """Upload an image to Imgur and return the image URL."""
    headers = {
        'Authorization': f'Client-ID {client_id}',
    }
    response = requests.post(
        'https://api.imgur.com/3/image',
        headers=headers,
        files={'image': image_file}
    )

    if response.status_code == 200:
        return response.json()['data']['link']
    else:
        print(f"Error uploading image: {response.json()}")
        return None