"""Import requests to receive request from the server."""
import requests
import logging


logger = logging.getLogger('Image to url')


def upload_image_to_imgur(image_file, client_id):
    """
    Upload an image to Imgur and return the image URL.

    :param image_file: Image file that return from a form.
    :param client_id: Imgur client_id

    """
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
        logger.error(f"Error uploading image: {response.json()}")
        raise FileNotFoundError
