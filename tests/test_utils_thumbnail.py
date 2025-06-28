import unittest
from unittest.mock import patch, MagicMock
from music.utils import thumbnail


class TestThumbnailUtils(unittest.TestCase):
    @patch('music.utils.thumbnail.requests.get')
    @patch('music.utils.thumbnail.create_temp_file')
    @patch('music.utils.thumbnail.get_logger')
    def test_download_thumbnail_success(self, mock_logger, mock_create_temp_file, mock_requests_get):
        mock_response = MagicMock()
        mock_response.content = b'data'
        mock_requests_get.return_value = mock_response
        mock_create_temp_file.return_value = '/tmp/fake.png'
        url = 'http://example.com/image.png'
        result = thumbnail.download_thumbnail(url)
        self.assertEqual(result, '/tmp/fake.png')
        mock_requests_get.assert_called_once_with(url)
        mock_create_temp_file.assert_called_once_with(b'data', suffix='.png')

    @patch('music.utils.thumbnail.MP3')
    @patch('music.utils.thumbnail.ID3')
    @patch('music.utils.thumbnail.Image.open')
    @patch('music.utils.thumbnail.get_logger')
    @patch('music.utils.thumbnail.open', create=True)
    @patch('music.utils.thumbnail.os.remove')
    def test_embed_thumbnail_success(self, mock_remove, mock_open, mock_logger, mock_image_open, mock_id3, mock_mp3):
        # Setup mocks
        mock_img = MagicMock()
        mock_img.format = 'JPEG'
        mock_image_open.return_value.__enter__.return_value = mock_img
        mock_audio = MagicMock()
        mock_mp3.return_value = mock_audio
        mock_audio.tags = MagicMock()
        mock_audio.tags.add = MagicMock()
        mock_audio.save = MagicMock()
        # Call function
        thumbnail.embed_thumbnail('audio.mp3', 'cover.jpg')
        mock_image_open.assert_called()
        mock_mp3.assert_called()
        mock_audio.save.assert_called()
        mock_remove.assert_called()


if __name__ == '__main__':
    unittest.main()
