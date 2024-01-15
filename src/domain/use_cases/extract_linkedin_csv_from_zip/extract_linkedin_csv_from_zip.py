from src.utils.file_handler import extract_files_from_zip


class LinkedinCsvDataExtractor:
    def __init__(self):
        self._interest_files = (
            "Connections.csv",
            "Shares.csv",
            "Comments.csv",
            "Reactions.csv",
        )

    def extract(self, zip_path: str, destine_folder: str):
        extract_files_from_zip(
            file_path=zip_path,
            destine_path=destine_folder,
            files_to_extract=self._interest_files,
        )
