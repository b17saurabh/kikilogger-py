import unittest
from unittest.mock import patch, mock_open

from src.kikiLogger.logger_factory import MultiAppenderLogger, getLogger


class TestLoggerFactory(unittest.TestCase):
    # @patch("builtins.open", mock_open(read_data='{"name": "test_logger"}'))
    def test_get_logger(self):

        #mock_open.return_value.read.return_value = '{"name": "test_logger", "appenders": [{"type": "console", "format": "%(levelname)s: %(message)s"}]}'

        logger = getLogger("test_logger_config.json")

        # Check that the logger is an instance of MultiAppenderLogger
        self.assertIsInstance(logger, MultiAppenderLogger)

        # Check that the logger has the correct name
        self.assertEqual(logger.name, "test_logger2")

        logger.info_async("test message")

        # Add more assertions as needed based on your specific requirements
        # For example, you can check if the logger has the correct level, appenders, etc.


if __name__ == "__main__":
    unittest.main()
