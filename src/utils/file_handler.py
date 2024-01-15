from zipfile import ZipFile


def extract_files_from_zip(file_path: str, destine_path: str, files_to_extract: list):
    with ZipFile(file_path, "r") as zObject:
        # zObject.extractall(path=destine_path)
        for file in files_to_extract:
            zObject.extract(file, path=destine_path)


def get_file_name_from_path(file_path: str):
    file_name = file_path.split("/")[-1]
    return file_name
