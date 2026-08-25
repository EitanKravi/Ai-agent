import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "The software executes Python code from the file located in the specified directory—relative to the working directory—",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file from which the content will be returned, relative to the working directory.",
                },
                "args": {
                    "type": "array",
                    "description": "The args if the python code need args",
                },
            },
        },
    },
}


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        # Give the abs path of the working_directory and the file
        working_dir_abs: str = os.path.abspath(working_directory)
        target_file: str = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file: bool = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

    except Exception as e:
        return f'Error: {e}'

    # Chack if the target_file is in working_dir_abs
    if not valid_target_file:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    # Chack if the target_file is a file
    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    # Chack if the target_file is a Python file
    if not target_file.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'

    # Make the command structure
    command = ["python", target_file]

    if args is not None:
        command.extend(args)

    try:
        # Execute the command
        result = subprocess.run(command,
                                cwd=working_dir_abs,
                                capture_output=True,
                                text=True,
                                timeout=30
                                )

        if result.returncode != 0:
            return f'Process exited with code {result.returncode}'

        if not result.stdout and not result.stderr:
            return "No output produced"

        output = []

        # add to output the stdout and stderr if exist
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")

        return "\n".join(output)

    except Exception as e:
        return f"Error: executing Python file: {e}"
