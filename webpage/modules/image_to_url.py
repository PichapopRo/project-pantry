import requests


def upload_image_to_imgur(image_path, client_id):
    """Upload an image to Imgur and return the image URL."""
    headers = {
        'Authorization': f'Client-ID {client_id}',
    }

    with open(image_path, 'rb') as image_file:
        response = requests.post(
            'https://api.imgur.com/3/image',
            headers=headers,
            data={'image': image_file.read()}
        )

    if response.status_code == 200:
        # Extract the URL from the response
        return response.json()['data']['link']
    else:
        print(f"Error uploading image: {response.json()}")
        return None