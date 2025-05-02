import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from unittest.mock import patch, MagicMock
import db

class TestDBFunctions(unittest.TestCase):
    @patch('db.connect_db')
    def test_check_credentials_success(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ('12345678', '1234')
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        result = db.check_credentials('12345678', '1234')
        self.assertTrue(result)

    @patch('db.connect_db')
    def test_check_credentials_fail(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        result = db.check_credentials('12345678', 'wrong')
        self.assertFalse(result)

    @patch('db.connect_db')
    def test_get_balance(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (100.0,)
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        result = db.get_balance('12345678')
        self.assertEqual(result, 100.0)

if __name__ == '__main__':
    unittest.main()
