import os
from config import MAX_CHARS

schema_get_files_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Returns the contents of the file in the directory specified relative to the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file from which the content will be returned, relative to the working directory.",
                },
            },
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        # Give the abs path of the working_directory and the file
        working_dir_abs: str = os.path.abspath(working_directory)
        target_file: str = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file: bool = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

    except Exception as e:
        return f'Error: {e}'

    # Chack if the target_file is in working_dir_abs
    if not valid_target_file:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    # Chack if the target_file is a file
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'


    try:
        with open(target_file, "r") as f:
            content = f.read(MAX_CHARS)

            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content

    except Exception as e:
        return f'Error: {e}'

