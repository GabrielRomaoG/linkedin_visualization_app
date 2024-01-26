from unittest.mock import Mock
import unittest
from src.domain.use_cases.extract_linkedin_csv_from_zip.extract_linkedin_csv_from_zip import (
    LinkedinCsvDataExtractor,
)


class TestLinkedinCsvDataExtractor(unittest.TestCase):
    def setUp(self):
        self.mock_extract_files_zip_func = Mock()
        self.use_case = LinkedinCsvDataExtractor(self.mock_extract_files_zip_func)

    def test_extract(self):
        # Setup
        zip_path = "test_zip.zip"
        destine_folder = "test_folder"

        # Exercise
        self.use_case.extract(zip_path, destine_folder)

        # Verify
        self.mock_extract_files_zip_func.assert_called_once_with(
            file_path=zip_path,
            destine_path=destine_folder,
            files_to_extract=self.use_case._LinkedinCsvDataExtractor__interest_files,
        )
