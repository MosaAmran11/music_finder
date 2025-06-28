import unittest
from music.utils.logger import get_logger
import logging


class TestLogger(unittest.TestCase):
    def test_get_logger_returns_logger_instance(self):
        logger = get_logger()
        self.assertIsInstance(logger, logging.Logger)

    def test_logger_logs_info(self):
        logger = get_logger()
        with self.assertLogs(logger, level='INFO') as cm:
            logger.info('Test log message')
        self.assertTrue(
            any('Test log message' in message for message in cm.output))


if __name__ == '__main__':
    unittest.main()
