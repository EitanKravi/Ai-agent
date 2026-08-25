import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "The operation overwrites the file content in the specified directory—relative to the working directory—with the new content.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file from which the content will be returned, relative to the working directory.",
                },
                "content": {
                    "type": "string",
                    "description": "The thing that will be written to the file in the specified directory relative to the working directory.",
                },
            },
        },
    },
}


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        # Give the abs path of the working_directory and the file
        working_dir_abs: str = os.path.abspath(working_directory)
        target_file: str = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file: bool = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

    except Exception as e:
        return f'Error: {e}'

    # Chack if the target_file is in working_dir_abs
    if not valid_target_file:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    # Chack if the target_file is a file
    if not os.path.isfile(target_file):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    try:
        # Create all parent directories if they don't exist
        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        with open(target_file, 'w') as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {e}'

