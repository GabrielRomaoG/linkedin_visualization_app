from src.utils.file_handler import extract_files_from_zip


class LinkedinCsvDataExtractor:
    def __init__(self, extract_files_zip_func=extract_files_from_zip):
        self.__extract_files_zip_func = extract_files_zip_func
        self.__interest_files = (
            "Connections.csv",
            "Shares.csv",
            "Comments.csv",
            "Reactions.csv",
        )

    def extract(self, zip_path: str, destine_folder: str):
        self.__extract_files_zip_func(
            file_path=zip_path,
            destine_path=destine_folder,
            files_to_extract=self._interest_files,
        )
