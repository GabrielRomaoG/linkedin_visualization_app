from zipfile import ZipFile


def extract_files_from_zip(file_path: str, destine_path: str, files_to_extract: list):
    with ZipFile(file_path, "r") as zObject:
        for file in files_to_extract:
            zObject.extract(file, path=destine_path)


def get_file_name_from_path(file_path: str):
    file_name = file_path.split("/")[-1]
    return file_name


def compare_file_names(file_name, interest_file_name):
    if file_name != interest_file_name:
        raise ValueError(
            f"File name '{file_name}' does not match the interest file name '{interest_file_name}'"
        )
