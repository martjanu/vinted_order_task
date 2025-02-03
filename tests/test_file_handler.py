import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../application')))

from unittest.mock import mock_open, patch
from file_handler import FileHandler


class TestFileHandler(unittest.TestCase):

    def setUp(self):
        self.file_handler = FileHandler(input_file='input.txt', output_file='output.txt', portion=3)

    def test_read_by_portion_success(self):
        mock_file_data = "line 1\nline 2\nline 3\nline 4\n"
        with patch("builtins.open", mock_open(read_data=mock_file_data)) as mocked_file:
            result = self.file_handler.read_by_portion()
            self.assertEqual(result, ['line 1', 'line 2', 'line 3'])
            mocked_file().seek.assert_called_once_with(0)

    def test_read_by_portion_file_not_found(self):
        with patch("builtins.open", side_effect=FileNotFoundError):
            result = self.file_handler.read_by_portion()
            self.assertEqual(result, "Error: The file 'input.txt' does not exist.")

    def test_write_to_file_success(self):
        with patch("builtins.open", mock_open()) as mock_file:
            result = self.file_handler.write_to_file('Test result')
            mock_file.assert_called_once_with('output.txt', 'a')
            mock_file().write.assert_called_once_with('Test result\n')

    def test_write_to_file_error(self):
        with patch("builtins.open", side_effect=Exception("Write Error")):
            result = self.file_handler.write_to_file('Test result')
            self.assertEqual(result, "Error writing to file: Write Error")

    def test_clear_output_success(self):
        with patch("builtins.open", mock_open()) as mock_file:
            result = self.file_handler.clear_output()
            mock_file.assert_called_once_with('output.txt', 'w')
            mock_file().write.assert_not_called()

    def test_clear_output_error(self):
        with patch("builtins.open", side_effect=Exception("Clear Error")):
            result = self.file_handler.clear_output()
            self.assertEqual(result, "Error clearing file: Clear Error")

    def test_process_reading_success(self):
        mock_file_data = "line 1\nline 2\nline 3\n"
        with patch("builtins.open", mock_open(read_data=mock_file_data)) as mocked_file:
            with patch.object(self.file_handler, '_check_end', return_value=False):
                mocked_file.return_value.seek = unittest.mock.MagicMock()
                result = self.file_handler._process_reading(mocked_file())
                self.assertEqual(result, ['line 1', 'line 2', 'line 3'])

    def test_check_end_true(self):
        result = self.file_handler._check_end(['line 1', 'line 2'])
        self.assertTrue(result)

    def test_check_end_false(self):
        result = self.file_handler._check_end(['line 1', 'line 2', 'line 3'])
        self.assertFalse(result)

    def test_read_method(self):
        mock_file_data = "line 1\nline 2\nline 3\nline 4\n"
        with patch("builtins.open", mock_open(read_data=mock_file_data)) as mocked_file:
            mocked_file.return_value.readline = unittest.mock.MagicMock(side_effect=["line 1", "line 2", "line 3", ""])
            result = self.file_handler._read(mocked_file())
            self.assertEqual(result, ['line 1', 'line 2', 'line 3'])

    def test_cursor_position_tracking(self):
        mock_file_data = "line 1\nline 2\nline 3\nline 4\n"
        with patch("builtins.open", mock_open(read_data=mock_file_data)) as mocked_file:
            mocked_file.return_value.tell = unittest.mock.MagicMock(return_value=14)
            self.file_handler.read_by_portion()
            self.assertEqual(self.file_handler.cursor_position, 14)

    def tearDown(self):
        del self.file_handler


if __name__ == '__main__':
    unittest.main()
