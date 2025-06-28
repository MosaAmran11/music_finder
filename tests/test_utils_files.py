import unittest
import os
from music.utils.files import create_temp_file


class TestCreateTempFile(unittest.TestCase):
    def test_create_temp_file_creates_file_with_content(self):
        content = b"test content"
        temp_path = create_temp_file(content, suffix='.test')
        self.assertTrue(os.path.exists(temp_path))
        with open(temp_path, 'rb') as f:
            self.assertEqual(f.read(), content)
        os.remove(temp_path)


if __name__ == '__main__':
    unittest.main()
