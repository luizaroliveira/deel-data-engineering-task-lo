import unittest
from unittest.mock import patch, mock_open, MagicMock

from database.models import ReportOperations
from operations.csv_report_generator import CSVReportGenerator
from sqlalchemy.orm import Session


class TestCSVReportGenerator(unittest.TestCase):

    def setUp(self):
        self.session_mock = MagicMock(spec=Session)
        self.report_operation_mock = MagicMock(spec=ReportOperations)
        self.report_operation_mock.report_description = "Test Report"
        self.chunk_size = 1000
        self.generator = CSVReportGenerator(self.session_mock, self.chunk_size)

    @patch('operations.csv_report_generator.shutil.move')
    @patch('operations.csv_report_generator.NamedTemporaryFile')
    @patch('operations.csv_report_generator.text')  # Mock sqlalchemy.text
    def test_export_csv_success(self, mock_text, mock_tempfile, mock_move):
        # Mock the temporary file
        mock_tempfile_instance = mock_tempfile.return_value.__enter__.return_value
        mock_tempfile_instance.name = "temp_file.csv"

        mock_result = MagicMock()
        mock_result.keys.return_value = ["col1", "col2"]
        mock_result.fetchmany.side_effect = [
            [("data1", "data2"), ("data3", "data4")],  # First chunk
            []  # No more data
        ]

        # Configure the mock text() function
        mock_text_instance = mock_text.return_value  # This represents the TextClause object
        self.session_mock.execute.return_value.__enter__.return_value = mock_result

        expected_csv_content = (
            "col1,col2\r\n"
            "data1,data2\r\n"
            "data3,data4\r\n"
        )

        m = mock_open()
        with patch('operations.csv_report_generator.open', m):
            result = self.generator.export_csv(self.report_operation_mock)

    @patch('operations.csv_report_generator.shutil.move')
    @patch('operations.csv_report_generator.NamedTemporaryFile')
    @patch('operations.csv_report_generator.text')  # Mock sqlalchemy.text
    def test_export_csv_no_data(self, mock_text, mock_tempfile, mock_move):
        mock_result = MagicMock()
        mock_result.fetchmany.return_value = []  # No data
        # Configure the mock text() function
        mock_text_instance = mock_text.return_value  # This represents the TextClause object
        self.session_mock.execute.return_value.__enter__.return_value = mock_result

        result = self.generator.export_csv(self.report_operation_mock)
        self.assertEqual(result["status"], "success")
        self.assertIn("found no data to be exported", result["message"])

    @patch('operations.csv_report_generator.shutil.move')
    @patch('operations.csv_report_generator.NamedTemporaryFile')
    def test_export_csv_exception(self, mock_tempfile, mock_move):
        mock_tempfile.side_effect = Exception("Test Exception")  # Simulate an error

        result = self.generator.export_csv(self.report_operation_mock)
        self.assertEqual(result["status"], "error")
        self.assertIn("Error exporting to CSV: Test Exception", result["message"])
