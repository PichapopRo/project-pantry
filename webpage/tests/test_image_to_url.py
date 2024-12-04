"""Tests for upload_image_to_imgur."""
from django.test import TestCase
from unittest.mock import patch, Mock
from webpage.modules.image_to_url import upload_image_to_imgur


class UploadImageToImgurTest(TestCase):
    """Test the upload_image_to_imgur."""

    @patch('requests.post')
    def test_upload_image_success(self, mock_post):
        """Test successful upload_image_to_imgur."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': {
                'link': 'https://imgur.com/success_image_url'
            }
        }
        mock_post.return_value = mock_response
        image_file = b'some_image_data'
        client_id = 'test_client_id'
        result = upload_image_to_imgur(image_file, client_id)
        self.assertEqual(result, 'https://imgur.com/success_image_url')
        mock_post.assert_called_once_with(
            'https://api.imgur.com/3/image',
            headers={'Authorization': 'Client-ID test_client_id'},
            files={'image': image_file}
        )

    @patch('requests.post')
    def test_upload_image_failure(self, mock_post):
        """Test failing upload_image_to_imgur."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            'data': {},
            'error': 'Bad request'
        }
        mock_post.return_value = mock_response
        image_file = b'some_image_data'
        client_id = 'test_client_id'
        self.assertRaises(FileNotFoundError, upload_image_to_imgur, image_file, client_id)
        mock_post.assert_called_once_with(
            'https://api.imgur.com/3/image',
            headers={'Authorization': 'Client-ID test_client_id'},
            files={'image': image_file}
        )
