import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../application')))

from datetime import datetime
from unittest.mock import MagicMock
from data_validator import DataValidator


class TestDataValidator(unittest.TestCase):
    def setUp(self):
        self.validator = DataValidator()

        self.mock_provider1 = MagicMock()
        self.mock_provider1.name = "Provider1"
        self.mock_provider1.sizes = ["S", "M"]

        self.mock_provider2 = MagicMock()
        self.mock_provider2.name = "Provider2"
        self.mock_provider2.sizes = ["L", "XL"]

        self.providers = [self.mock_provider1, self.mock_provider2]

    def test_valid_format(self):
        line = "2025-02-01 S Provider1"
        result = self.validator.process_validation(line, self.providers)
        self.assertEqual(result, line)

    def test_invalid_format(self):
        line = "2025-02-01 S"
        result = self.validator.process_validation(line, self.providers)
        self.assertEqual(result, f"{line} Ignored")

    def test_valid_date(self):
        line = "2025-02-01 S Provider1"
        result = self.validator.process_validation(line, self.providers)
        self.assertEqual(result, line)

    def test_invalid_date(self):
        line = "2025-02-30 S Provider1"
        result = self.validator.process_validation(line, self.providers)
        self.assertEqual(result, f"{line} Ignored")

    def test_valid_size(self):
        line = "2025-02-01 S Provider1"
        result = self.validator.process_validation(line, self.providers)
        self.assertEqual(result, line)

    def test_invalid_size(self):
        line = "2025-02-01 XL Provider1"
        result = self.validator.process_validation(line, self.providers)
        self.assertEqual(result, f"{line} Ignored")

    def test_valid_provider(self):
        line = "2025-02-01 S Provider1"
        result = self.validator.process_validation(line, self.providers)
        self.assertEqual(result, line)

    def test_invalid_provider(self):
        line = "2025-02-01 S Provider3"
        result = self.validator.process_validation(line, self.providers)
        self.assertEqual(result, f"{line} Ignored")

    def test_all_invalid_conditions(self):
        line = "2025-02-30 XL Provider3"
        result = self.validator.process_validation(line, self.providers)
        self.assertEqual(result, f"{line} Ignored")

    def tearDown(self):
        del self.validator
        del self.providers


if __name__ == '__main__':
    unittest.main()
